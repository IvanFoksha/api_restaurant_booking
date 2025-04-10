from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.table import TableCreate, TableResponse, TableUpdate
from app.services.table import TableService

router = APIRouter()


@router.get("/", response_model=List[TableResponse])
def get_tables(
    session: Session = Depends(get_session)
) -> List[TableResponse]:
    """
    Get all tables.
    """
    service = TableService(session)
    return service.get_all()


@router.post("/", response_model=TableResponse, status_code=status.HTTP_201_CREATED)
def create_table(
    table_data: TableCreate,
    session: Session = Depends(get_session)
) -> TableResponse:
    """
    Create a new table.
    """
    service = TableService(session)
    table = service.create(table_data)
    if not table:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create table"
        )
    return table


@router.get("/{table_id}", response_model=TableResponse)
def get_table(
    table_id: int,
    session: Session = Depends(get_session)
) -> TableResponse:
    """
    Get table by ID.
    """
    service = TableService(session)
    table = service.get_by_id(table_id)
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Table with ID {table_id} not found"
        )
    return table


@router.put("/{table_id}", response_model=TableResponse)
def update_table(
    table_id: int,
    table_data: TableUpdate,
    session: Session = Depends(get_session)
) -> TableResponse:
    """
    Update an existing table.
    """
    service = TableService(session)
    table = service.update(table_id, table_data)
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Table with ID {table_id} not found"
        )
    return table


@router.delete("/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_table(
    table_id: int,
    session: Session = Depends(get_session)
) -> None:
    """
    Delete a table.
    """
    service = TableService(session)
    if not service.delete(table_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Table with ID {table_id} not found"
        )
