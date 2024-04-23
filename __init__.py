import os
from flask import *
import apps.llm as llm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from apps.login_process import login_required
from models.sqlmodels import *
from models.formModels import *
from apps.get import *
from apps.login_process import *
from apps.randomprofile import *
import hashlib

app = Flask(__name__)