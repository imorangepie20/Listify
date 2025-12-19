#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Auth API 테스트 스크립트
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_register():
    """회원가입 테스트"""
    print("=== 회원가입 테스트 ===")

    data = {
        "email": "test@example.com",
        "password": "test123!",
        "nickname": "테스트유저"
    }

    response = requests.post(f"{BASE_URL}/auth/register", json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

    return response.status_code == 200

def test_login():
    """로그인 테스트"""
    print("=== 로그인 테스트 ===")

    data = {
        "email": "test@example.com",
        "password": "test123!"
    }

    response = requests.post(f"{BASE_URL}/auth/login", json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

    if response.status_code == 200:
        token = response.json()["data"]["access_token"]
        return token
    return None

def test_verify_token(token):
    """토큰 검증 테스트"""
    print("=== 토큰 검증 테스트 ===")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(f"{BASE_URL}/auth/verify", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

    return response.status_code == 200

def test_health():
    """헬스체크 테스트"""
    print("=== 헬스체크 테스트 ===")

    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

if __name__ == "__main__":
    try:
        # 헬스체크 먼저
        test_health()

        # 회원가입 테스트
        register_success = test_register()

        # 로그인 테스트
        if register_success:
            token = test_login()

            # 토큰 검증 테스트
            if token:
                test_verify_token(token)

        print("✅ 모든 테스트 완료!")

    except Exception as e:
        print(f"❌ 테스트 중 오류 발생: {e}")