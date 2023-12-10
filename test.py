from fastapi import FastAPI, Path, HTTPException, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import Optional, Dict
from pydantic import BaseModel
import mood_analized.predict as predict 
import music_creater.Generate as Generate
import uvicorn
import psutil
import os
import asyncio

Generate.gen_music([])
