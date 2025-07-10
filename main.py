from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from agents import Agent, AsyncOpenAI,OpenAIChatCompletionsModel,Runner


app = FastAPI()
templates = Jinja2Templates(directory="templates")



client = AsyncOpenAI(
     api_key="AIzaSyCMpBWF-tOzuVQ9inIyVlPo7VFCJ6b9dd0",
     base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client
)
history_teacher = Agent(name="history_teacher", instructions="You are specialist in history", model=model)


# ✅ Home GET route
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )

# ✅ Home POST route with agent response
@app.post("/", response_class=HTMLResponse)
async def home(request: Request, prompt: str = Form(...)):
    print("User said:", prompt)
    
 
    response = await Runner.run(history_teacher, prompt)
    final_result = response.final_output
    return templates.TemplateResponse(
        request=request, name="index.html", context={"name": final_result}
    )
