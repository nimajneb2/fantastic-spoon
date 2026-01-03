#!/usr/bin/env python3
"""
Simple test script to verify Rebrickable API integration
"""
from rebrickable_api import RebrickableAPI


def test_api():
    api = RebrickableAPI()
    
    print("Testing Rebrickable API Integration\n")
    print("=" * 50)
    
    print("\n1. Testing Part Search (part_num=3001)...")
    result = api.get_part('3001')
    if 'error' in result:
        print(f"   Error: {result['error']}")
    else:
        print(f"   ✓ Found: {result.get('name', 'Unknown')}")
        print(f"   Part Number: {result.get('part_num', 'N/A')}")
    
    print("\n2. Testing Element Search (element_id=300121)...")
    result = api.get_element('300121')
    if 'error' in result:
        print(f"   Error: {result['error']}")
    else:
        print(f"   ✓ Element ID: {result.get('element_id', 'N/A')}")
        if 'part' in result:
            print(f"   Part: {result['part'].get('name', 'N/A')}")
        if 'color' in result:
            print(f"   Color: {result['color'].get('name', 'N/A')}")
    
    print("\n3. Testing Part Colors (part_num=3001)...")
    result = api.get_part_colors('3001')
    if 'error' in result:
        print(f"   Error: {result['error']}")
    else:
        count = len(result.get('results', []))
        print(f"   ✓ Found {count} color variants")
    
    print("\n4. Testing Invalid Part Number...")
    result = api.get_part('invalid-part-12345')
    if 'error' in result:
        print(f"   ✓ Error handling works: {result['error']}")
    else:
        print(f"   Unexpected success")
    
    print("\n" + "=" * 50)
    print("API Integration Test Complete!")


if __name__ == '__main__':
    test_api()
