import psycopg2
import re
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_schema():

    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    
    cursor = conn.cursor()
    

    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    tables = [table[0] for table in cursor.fetchall()]
    
    schema_info = {}
    
    # For each table, get columns and their data types
    for table in tables:
        cursor.execute(f"""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = '{table}'
            ORDER BY ordinal_position
        """)
        columns = cursor.fetchall()
        
        schema_info[table] = {
            "columns": [{"name": col[0], "type": col[1], "nullable": col[2]} for col in columns],
            "relationships": []
        }
    
    # Get foreign key relationships
    cursor.execute("""
        SELECT
            tc.table_name, 
            kcu.column_name, 
            ccu.table_name AS foreign_table_name,
            ccu.column_name AS foreign_column_name 
        FROM information_schema.table_constraints AS tc 
        JOIN information_schema.key_column_usage AS kcu
          ON tc.constraint_name = kcu.constraint_name
        JOIN information_schema.constraint_column_usage AS ccu 
          ON ccu.constraint_name = tc.constraint_name
        WHERE constraint_type = 'FOREIGN KEY'
    """)
    
    relationships = cursor.fetchall()
    
    # Add relationships to their respective tables
    for rel in relationships:
        table, column, foreign_table, foreign_column = rel
        if table in schema_info:
            schema_info[table]["relationships"].append({
                "column": column,
                "references": f"{foreign_table}.{foreign_column}"
            })
    
    cursor.close()
    conn.close()
    
    return schema_info






def format_schema_for_prompt(schema_info):
    prompt_text = "DATABASE SCHEMA:\n\n"
    
    # Format tables and columns
    for table, info in schema_info.items():
        prompt_text += f"Table: {table}\n"
        prompt_text += "Columns:\n"
        for column in info["columns"]:
            nullable = "NULL" if column["nullable"] == "YES" else "NOT NULL"
            prompt_text += f"  - {column['name']} ({column['type']}, {nullable})\n"
        
        # Add relationships if they exist
        if info["relationships"]:
            prompt_text += "Relationships:\n"
            for rel in info["relationships"]:
                prompt_text += f"  - {rel['column']} → {rel['references']}\n"
        
        prompt_text += "\n"
    
    return prompt_text




def update_config_file(schema_prompt):
    with open('config/config.py', 'r') as file:
        content = file.read()
    
    # Define pattern to find the system prompt variable
    pattern = r'(SYSTEM_PROMPT\s*=\s*""".*?""")'
    
    # Check if there's already a DATABASE SCHEMA section
    if 'DATABASE SCHEMA:' in content:
        # Replace the existing schema
        pattern_with_schema = r'(DATABASE SCHEMA:.*?)(?=\n\n[A-Z]|""")'
        content = re.sub(pattern_with_schema, schema_prompt.strip(), content, flags=re.DOTALL)
    else:
        # Insert the schema into the system prompt
        replacement = f'SYSTEM_PROMPT = """{schema_prompt}\n\\1'
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open('config.py', 'w') as file:
        file.write(content)


def update_DB_Schema():
    schema_info = get_db_schema()
    schema_prompt = format_schema_for_prompt(schema_info)
    update_config_file(schema_prompt)