from fastapi import APIRouter, HTTPException, status

from core.config import DNK

router = APIRouter()


@router.post('/check')
async def create(codon):
    if len(codon) > 3:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Кодон может состоять только из 3 символов')
    for key in codon:
        if key.lower() not in ['a', 'c', 'g', 't']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Кодон может содержать только буквы '
                                                                                'A, C, G, T англисйкого алфавита')
    return {'codon': codon in DNK}