from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.text_extraction import extract_text
from app.services.chunking import fixed_size_chunking, sentence_based_chunking
from app.services.embedding import store_chunks
from app.services.sql_db import init_db, insert_metadata

router = APIRouter()

# Initiate database
init_db()

# Upload file as .txt or .pdf
@router.post('/upload')
async def upload_document(file : UploadFile = File(...), chunk_method: str = "fixed"):

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

    # Selectable chunking method (can improve the query later)
    try:
        if chunk_method == "sentence":    
            chunks = sentence_based_chunking(text)
            
        else:
            chunks = fixed_size_chunking(text)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading chunks {str(e)}")


    # Generate metadata for each chunk
    metadata = [
        {"filename":file.filename, "chunk_index": idx,"text_preview": chunk[:100]}
        for idx, chunk in enumerate(chunks)
    ]

    # upsert to Qdrant
    store_chunks(chunks, metadata)

    # Insert to SQL database
    insert_metadata(metadata)

    # Return response
    return {"filename": file.filename,
            "num_chunks": len(chunks),
            "chunk_method": chunk_method,
            "chunk_preview" : chunks[:2],
            "stored_in_qdrant": True
        }




