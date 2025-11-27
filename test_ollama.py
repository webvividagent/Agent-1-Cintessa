#!/usr/bin/env python3
import ollama
import sys

print("🔍 Testing Ollama connection...")

try:
    # Test basic connection
    print("1. Testing Ollama list...")
    models = ollama.list()
    print(f"✅ Success! Found {len(models['models'])} models:")
    
    for model in models['models']:
        print(f"   - {model['name']}")
    
    # Test if we can use a model
    print("\n2. Testing model response...")
    test_response = ollama.chat(
        model=models['models'][0]['name'], 
        messages=[{'role': 'user', 'content': 'Say hello in one word.'}]
    )
    print(f"✅ Model response: {test_response['message']['content']}")
    
    print("\n🎉 All tests passed! Ollama is working correctly.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n💡 Troubleshooting tips:")
    print("   - Make sure Ollama is running: ollama serve")
    print("   - Check if models are downloaded: ollama list")
    print("   - Verify Ollama service: curl http://localhost:11434/api/tags")
