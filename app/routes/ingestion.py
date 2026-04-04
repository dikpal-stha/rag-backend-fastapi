from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.text_extraction import extract_text
from app.services.chunking import fixed_size_chunking

router = APIRouter()

# testing
@router.get('/')
def test_ingestion():
    return {"message": "ingestion route works perfectly!"}

# Upload file as .txt or .pdf
@router.post('/upload')
async def upload_document(file : UploadFile = File(...)):

    # check the file format
    if not(file.filename.endswith(".txt") or (file.filename.endswith(".pdf"))):
        raise HTTPException(status_code=400, detail="Unsupported file type")
    

    # save the file temporarily
    try:
        contents = await file.read()
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(contents)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File could not be saved, {str(e)}")
    

    # Extract text
    try:
        text = extract_text(temp_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file {str(e)}")

    # applying fixed chunking method
    try:    
        chunks = fixed_size_chunking(text)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading chunks {str(e)}")


    return {"filename": file.filename, "num_chunks": len(chunks), "chunk_preview" : chunks[:2]}




