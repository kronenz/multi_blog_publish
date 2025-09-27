from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from backend.src.models.knowledge_vault import KnowledgeVault
from backend.src.services.knowledge_vault_service import KnowledgeVaultService

router = APIRouter()
knowledge_vault_service = KnowledgeVaultService()

@router.post("/knowledge_vaults", response_model=KnowledgeVault, status_code=201)
def create_knowledge_vault(knowledge_vault: KnowledgeVault):
    return knowledge_vault_service.create_knowledge_vault(knowledge_vault)

@router.get("/knowledge_vaults/{knowledge_vault_id}", response_model=KnowledgeVault)
def get_knowledge_vault(knowledge_vault_id: UUID):
    knowledge_vault = knowledge_vault_service.get_knowledge_vault_by_id(knowledge_vault_id)
    if knowledge_vault is None:
        raise HTTPException(status_code=404, detail="Knowledge vault not found")
    return knowledge_vault
