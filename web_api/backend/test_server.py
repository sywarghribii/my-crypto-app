"""
Simple test API to verify FastAPI is working
"""
from fastapi import FastAPI

app = FastAPI(title="ML Analytics API - Test")

@app.get("/")
def read_root():
    return {
        "status": "✓ API is working!",
        "message": "FastAPI server is running successfully"
    }

@app.get("/test")
def test_endpoint():
    return {"test": "success"}

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("  Starting FastAPI Server...")
    print("  URL: http://127.0.0.1:8080")
    print("  Docs: http://127.0.0.1:8080/docs")
    print("="*60 + "\n")
    uvicorn.run(app, host="127.0.0.1", port=8080)
