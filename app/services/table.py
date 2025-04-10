from typing import List, Optional

from sqlmodel import Session, select

from app.models.table import Table
from app.schemas.table import TableCreate, TableUpdate


class TableService:
    """
    Service for managing restaurant tables.
    """

    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Table]:
        """
        Get all tables.
        
        Returns:
            List[Table]: List of all tables
        """
        statement = select(Table)
        return self.session.exec(statement).all()

    def get_by_id(self, table_id: int) -> Optional[Table]:
        """
        Get table by ID.
        
        Args:
            table_id: Table ID
            
        Returns:
            Optional[Table]: Table if found, None otherwise
        """
        return self.session.get(Table, table_id)

    def create(self, table_data: TableCreate) -> Table:
        """
        Create a new table.
        
        Args:
            table_data: Table data
            
        Returns:
            Table: Created table
        """
        table = Table(**table_data.model_dump())
        self.session.add(table)
        self.session.commit()
        self.session.refresh(table)
        return table

    def update(self, table_id: int, table_data: TableUpdate) -> Optional[Table]:
        """
        Update an existing table.
        
        Args:
            table_id: Table ID
            table_data: Updated table data
            
        Returns:
            Optional[Table]: Updated table if found, None otherwise
        """
        table = self.get_by_id(table_id)
        if not table:
            return None

        update_data = table_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(table, key, value)

        self.session.add(table)
        self.session.commit()
        self.session.refresh(table)
        return table

    def delete(self, table_id: int) -> bool:
        """
        Delete a table.
        
        Args:
            table_id: Table ID
            
        Returns:
            bool: True if table was deleted, False otherwise
        """
        table = self.get_by_id(table_id)
        if not table:
            return False

        self.session.delete(table)
        self.session.commit()
        return True

    def get_available_tables(self, seats: int) -> List[Table]:
        """
        Get tables with sufficient seats.
        
        Args:
            seats: Required number of seats
            
        Returns:
            List[Table]: List of available tables
        """
        statement = select(Table).where(Table.seats >= seats)
        return self.session.exec(statement).all() 