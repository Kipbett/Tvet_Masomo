import uuid
from celery import shared_task
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import time
from .mpesa_utils.plan_generater import generate_learning_plan_doc  # <-- your OpenAI + docx function

@shared_task(bind=True)
def generate_plan_task(self, curriculum_content, os_content, weeks, sessions, hours):
    try:
        # Step 1: Parsing files
        self.update_state(state="PROGRESS", meta={"step": "Parsing uploaded files..."})
        time.sleep(1)

        # Step 2: Call AI to generate learning plan (Word document bytes)
        self.update_state(state="PROGRESS", meta={"step": "Generating learning plan with AI..."})
        docx_bytes = generate_learning_plan_doc(curriculum_content, os_content, weeks, sessions, hours)

        # Step 3: Save file
        self.update_state(state="PROGRESS", meta={"step": "Formatting and saving document..."})
        filename = f"learning_plan_{uuid.uuid4().hex}.docx"
        file_path = f"plans/{filename}"
        default_storage.save(file_path, ContentFile(docx_bytes))

        return {"status": "completed", "file_path": file_path, "filename": filename}

    except Exception as e:
        return {"status": "failed", "error": str(e)}