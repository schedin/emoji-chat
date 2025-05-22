#!/usr/bin/env python3
"""Simple test script for the emoji chat backend API."""

import asyncio
import httpx
import json
from config import settings


async def test_health_endpoint():
    """Test the health endpoint."""
    print("Testing health endpoint...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"http://{settings.host}:{settings.port}/health")
            print(f"Health check status: {response.status_code}")
            if response.status_code == 200:
                print(f"Response: {response.json()}")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Health check failed: {e}")


async def test_emoji_endpoint():
    """Test the emoji generation endpoint."""
    print("\nTesting emoji generation endpoint...")
    
    test_messages = [
        "I'm so happy today!",
        "It's raining outside",
        "I love pizza",
        "Good morning everyone"
    ]
    
    async with httpx.AsyncClient() as client:
        for message in test_messages:
            try:
                print(f"\nTesting message: '{message}'")
                response = await client.post(
                    f"http://{settings.host}:{settings.port}/api/emojis",
                    json={"message": message},
                    timeout=30.0
                )
                
                print(f"Status: {response.status_code}")
                if response.status_code == 200:
                    result = response.json()
                    print(f"Emojis: {result['emojis']}")
                    print(f"Moderation passed: {result.get('moderation_passed', 'N/A')}")
                else:
                    print(f"Error: {response.text}")
                    
            except Exception as e:
                print(f"Request failed: {e}")


async def test_invalid_requests():
    """Test invalid request handling."""
    print("\nTesting invalid requests...")
    
    invalid_tests = [
        {"message": ""},  # Empty message
        {"message": "x" * 2000},  # Too long message
        {},  # Missing message field
    ]
    
    async with httpx.AsyncClient() as client:
        for i, test_data in enumerate(invalid_tests):
            try:
                print(f"\nInvalid test {i+1}: {test_data}")
                response = await client.post(
                    f"http://{settings.host}:{settings.port}/api/emojis",
                    json=test_data,
                    timeout=30.0
                )
                
                print(f"Status: {response.status_code}")
                print(f"Response: {response.text}")
                
            except Exception as e:
                print(f"Request failed: {e}")


async def main():
    """Run all tests."""
    print("Starting API tests...")
    print(f"Server: http://{settings.host}:{settings.port}")
    print(f"LLM URL: {settings.llm_url}")
    print(f"Content moderation: {settings.enable_content_moderation}")
    
    await test_health_endpoint()
    await test_emoji_endpoint()
    await test_invalid_requests()
    
    print("\nTests completed!")


if __name__ == "__main__":
    asyncio.run(main())
