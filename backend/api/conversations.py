# # backend/api/conversations.py
# from fastapi import APIRouter, Depends, HTTPException
# from motor.motor_asyncio import AsyncIOMotorClient
# from typing import List
# from pydantic import BaseModel, Field
# import datetime

# from backend.db.mongodb import get_mongo_db
# from backend.models.user import User
# from backend.api.auth_utils import get_current_user # Using the insecure one for now

# router = APIRouter()

# # Pydantic model for the response to ensure type safety
# class ConversationPreview(BaseModel):
#     id: str = Field(..., alias="_id")
#     title: str
#     created_at: datetime.datetime

#     # class Config:
#     #     allow_population_by_field_name = True
#     #     json_encoders = {
#     #        # MongoDB stores ObjectIDs, we need to convert them to strings for JSON
#     #        'id': lambda v: str(v),
#     #     }
#     model_config = {
#         "populate_by_name": True,
#     }

# @router.get("/conversations", response_model=List[ConversationPreview])
# async def get_user_conversations(
#     current_user: User = Depends(get_current_user),
#     mongo_db: AsyncIOMotorClient = Depends(get_mongo_db)
# ):
#     """
#     Fetches all conversations for the current user.
#     The 'title' is generated from the user's first message.
#     """
#     conversations_cursor = mongo_db.conversations.find(
#         {"user_id": str(current_user.id)},
#         # Projection: only get necessary fields
#         {"messages": {"$slice": 1}, "created_at": 1} 
#     )
    
#     results = []
#     async for convo in conversations_cursor:
#         first_message = "New Conversation"
#         if convo.get("messages"):
#             # Find the first message from the user to use as a title
#             user_message = next((msg for msg in convo["messages"] if msg.get("role") == "user"), None)
#             if user_message:
#                 # Truncate for a short title
#                 first_message = (user_message["message"][:40] + '...') if len(user_message["message"]) > 40 else user_message["message"]

#         results.append({
#             "_id": str(convo["_id"]),
#             "title": first_message,
#             "created_at": convo["created_at"]
#         })

#     return results
# backend/api/conversations.py
import datetime
import csv
import io
from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.responses import StreamingResponse
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
from pydantic import BaseModel, Field
from bson import ObjectId

from backend.db.mongodb import get_mongo_db
from backend.models.user import User
from backend.api.auth_utils import get_current_user_from_query, get_current_user

router = APIRouter()

# --- Pydantic Schemas for this file ---

class ConversationSummary(BaseModel):
    # The response_model now validates against this shape.
    # We no longer need the alias here since we are building the dict manually.
    id: str
    title: str
    summary: str
    created_at: datetime.datetime

    class Config:
        arbitrary_types_allowed = True
        json_encoders = { ObjectId: str }

class Message(BaseModel):
    role: str
    message: str

class ConversationDetail(ConversationSummary):
    messages: List[Message]

# --- API Endpoints ---

@router.get("/conversations", response_model=List[ConversationSummary])
async def get_user_conversations(
    current_user: User = Depends(get_current_user_from_query),
    mongo_db: AsyncIOMotorClient = Depends(get_mongo_db)
):
    """
    Fetches summaries of all conversations for the current user.
    """
    conversations_cursor = mongo_db.conversations.find(
        {"user_id": str(current_user.id)},
        {"messages": 1, "created_at": 1, "title": 1, "summary": 1}
    ).sort("created_at", -1)
    
    results = []
    async for convo in conversations_cursor:
        # --- THIS IS THE FINAL FIX ---
        # We will build a plain Python dictionary with the EXACT keys the frontend expects.
        # This removes all ambiguity from Pydantic's aliasing and serialization.
        
        title = convo.get("title")
        messages = convo.get("messages", [])
        if not title and messages:
            first_message = messages[0].get("message", "")
            title = (first_message[:40] + '...') if len(first_message) > 40 else first_message
        
        summary = convo.get("summary")
        if not summary and messages:
            ai_responses = [msg["message"] for msg in messages if msg.get("role") == "ai"]
            if ai_responses:
                first_response = ai_responses[0]
                summary = (first_response[:70] + '...') if len(first_response) > 70 else first_response

        # Create the dictionary with the 'id' key directly.
        clean_data = {
            "id": str(convo["_id"]), # Use the desired frontend key name 'id'
            "title": title or "Untitled Chat",
            "summary": summary or "",
            "created_at": convo["created_at"]
        }
        results.append(clean_data)
        # --- END FIX ---

    return results

@router.get("/conversations/{convo_id}", response_model=ConversationDetail)
async def get_conversation_details(
    convo_id: str,
    current_user: User = Depends(get_current_user_from_query),
    mongo_db: AsyncIOMotorClient = Depends(get_mongo_db)
):
    if not ObjectId.is_valid(convo_id):
        raise HTTPException(status_code=400, detail="Invalid conversation ID format.")

    convo = await mongo_db.conversations.find_one(
        {"_id": ObjectId(convo_id), "user_id": str(current_user.id)}
    )

    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found.")
    
    # We must also rename the _id to id before returning the raw dict
    # so it matches the ConversationDetail Pydantic model.
    convo["id"] = str(convo["_id"])
    del convo["_id"]
    
    if not convo.get("title"):
        convo["title"] = "Untitled Chat"
    if not convo.get("summary"):
        messages = convo.get("messages", [])
        convo["summary"] = (messages[1]["message"][:70] + '...') if len(messages) > 1 else ""

    return convo


# ... (The rest of your endpoints remain unchanged) ...
@router.put("/conversations/{convo_id}/title")
async def update_conversation_title(
    convo_id: str,
    new_title: str = Body(..., embed=True), 
    current_user: User = Depends(get_current_user),
    mongo_db: AsyncIOMotorClient = Depends(get_mongo_db)
):
    if not ObjectId.is_valid(convo_id):
        raise HTTPException(status_code=400, detail="Invalid conversation ID format.")
    
    result = await mongo_db.conversations.update_one(
        {"_id": ObjectId(convo_id), "user_id": str(current_user.id)},
        {"$set": {"title": new_title}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Conversation not found or permission denied.")
    return {"message": "Title updated successfully."}


@router.delete("/conversations/{convo_id}", status_code=204)
async def delete_conversation(
    convo_id: str,
    current_user: User = Depends(get_current_user_from_query),
    mongo_db: AsyncIOMotorClient = Depends(get_mongo_db)
):
    if not ObjectId.is_valid(convo_id):
        raise HTTPException(status_code=400, detail="Invalid conversation ID format.")
        
    result = await mongo_db.conversations.delete_one(
        {"_id": ObjectId(convo_id), "user_id": str(current_user.id)}
    )
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Conversation not found or permission denied.")
    return None


@router.get("/conversations/{convo_id}/export/csv")
async def export_conversation_csv(
    convo_id: str,
    current_user: User = Depends(get_current_user_from_query),
    mongo_db: AsyncIOMotorClient = Depends(get_mongo_db)
):
    convo = await mongo_db.conversations.find_one(
        {"_id": ObjectId(convo_id), "user_id": str(current_user.id)}
    )
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found.")

    string_io = io.StringIO()
    writer = csv.writer(string_io)
    writer.writerow(["User Question", "AI Response"])

    messages = convo.get("messages", [])
    for i in range(0, len(messages) - 1, 2):
        if i+1 < len(messages) and messages[i].get("role") == "user" and messages[i+1].get("role") == "ai":
            writer.writerow([messages[i].get("message"), messages[i+1].get("message")])
    
    string_io.seek(0)
    
    response = StreamingResponse(string_io, media_type="text/csv")
    response.headers["Content-Disposition"] = f"attachment; filename=conversation_{convo_id}.csv"
    return response