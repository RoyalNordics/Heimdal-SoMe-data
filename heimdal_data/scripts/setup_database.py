#!/usr/bin/env python3
"""
Script to set up a PostgreSQL database for the Heimdal SoMe Data Collection module.
"""

import os
import sys
import argparse
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
from pathlib import Path

# Add the parent directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Load environment variables
load_dotenv()

def create_database(host, port, user, password, dbname):
    """
    Create a PostgreSQL database.
    
    Args:
        host (str): Database host
        port (str): Database port
        user (str): Database user
        password (str): Database password
        dbname (str): Database name
    
    Returns:
        bool: True if the database was created successfully, False otherwise
    """
    # Connect to the default database
    conn = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        dbname="postgres"
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    try:
        # Check if the database already exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (dbname,))
        if cursor.fetchone():
            print(f"Database '{dbname}' already exists")
            return True
        
        # Create the database
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))
        print(f"Database '{dbname}' created successfully")
        return True
    except Exception as e:
        print(f"Error creating database: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def create_tables(host, port, user, password, dbname):
    """
    Create tables in the PostgreSQL database.
    
    Args:
        host (str): Database host
        port (str): Database port
        user (str): Database user
        password (str): Database password
        dbname (str): Database name
    
    Returns:
        bool: True if the tables were created successfully, False otherwise
    """
    # Import the database models
    from heimdal_data.database.models import Base
    from sqlalchemy import create_engine
    
    # Create the database URL
    database_url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    
    try:
        # Create the SQLAlchemy engine
        engine = create_engine(database_url)
        
        # Create the tables
        Base.metadata.create_all(engine)
        print(f"Tables created successfully in database '{dbname}'")
        return True
    except Exception as e:
        print(f"Error creating tables: {e}")
        return False

def update_env_file(host, port, user, password, dbname):
    """
    Update the .env file with the database connection details.
    
    Args:
        host (str): Database host
        port (str): Database port
        user (str): Database user
        password (str): Database password
        dbname (str): Database name
    
    Returns:
        bool: True if the .env file was updated successfully, False otherwise
    """
    env_file = Path(__file__).parent.parent / ".env"
    
    try:
        # Read the current .env file
        with open(env_file, 'r') as f:
            lines = f.readlines()
        
        # Update the database connection details
        updated_lines = []
        for line in lines:
            if line.startswith("DB_HOST="):
                updated_lines.append(f"DB_HOST={host}\n")
            elif line.startswith("DB_PORT="):
                updated_lines.append(f"DB_PORT={port}\n")
            elif line.startswith("DB_NAME="):
                updated_lines.append(f"DB_NAME={dbname}\n")
            elif line.startswith("DB_USER="):
                updated_lines.append(f"DB_USER={user}\n")
            elif line.startswith("DB_PASSWORD="):
                updated_lines.append(f"DB_PASSWORD={password}\n")
            elif line.startswith("TESTING="):
                updated_lines.append("TESTING=false\n")
            else:
                updated_lines.append(line)
        
        # Write the updated .env file
        with open(env_file, 'w') as f:
            f.writelines(updated_lines)
        
        print(f".env file updated successfully")
        return True
    except Exception as e:
        print(f"Error updating .env file: {e}")
        return False

def main():
    """
    Main function.
    """
    parser = argparse.ArgumentParser(description="Set up a PostgreSQL database for the Heimdal SoMe Data Collection module")
    parser.add_argument("--host", default=os.getenv("DB_HOST", "localhost"), help="Database host")
    parser.add_argument("--port", default=os.getenv("DB_PORT", "5432"), help="Database port")
    parser.add_argument("--user", default=os.getenv("DB_USER", "postgres"), help="Database user")
    parser.add_argument("--password", default=os.getenv("DB_PASSWORD", "postgres"), help="Database password")
    parser.add_argument("--dbname", default=os.getenv("DB_NAME", "heimdal_some_data"), help="Database name")
    parser.add_argument("--update-env", action="store_true", help="Update the .env file with the database connection details")
    
    args = parser.parse_args()
    
    print(f"Setting up PostgreSQL database '{args.dbname}' on {args.host}:{args.port}")
    
    # Create the database
    if create_database(args.host, args.port, args.user, args.password, args.dbname):
        # Create the tables
        if create_tables(args.host, args.port, args.user, args.password, args.dbname):
            print("Database setup completed successfully")
            
            # Update the .env file if requested
            if args.update_env:
                if update_env_file(args.host, args.port, args.user, args.password, args.dbname):
                    print("Environment variables updated successfully")
                else:
                    print("Failed to update environment variables")
        else:
            print("Failed to create tables")
    else:
        print("Failed to create database")

if __name__ == "__main__":
    main()
