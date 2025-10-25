import re
import os

files = [
    'app/color/page.tsx',
    'app/simple/page.tsx',
    'app/sprint/page.tsx',
    'app/dual/page.tsx',
    'app/ranking/page.tsx'
]

# パターン1: useEffect内でgetUser()を直接使用している
pattern1 = r'useEffect\(\(\) => \{\s*const currentUser = getUser\(\);'
replacement1 = '''useEffect(() => {
    const loadUser = async () => {
      const currentUser = await getUser();'''

# パターン2: useEffect内でgetUser()を使った後のsetUserまで
pattern2 = r'(useEffect\(\(\) => \{\s*)const currentUser = getUser\(\);(\s*if \(!currentUser\) \{[^}]*\}\s*setUser\(currentUser\);)(\s*\}, \[)'

def fix_pattern2(match):
    return f'''{match.group(1)}const loadUser = async () => {{
      const currentUser = await getUser();{match.group(2)}
    }};
    loadUser();{match.group(3)}'''

for file in files:
    if not os.path.exists(file):
        print(f"Skipping {file} (not found)")
        continue
    
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # パターン2の修正（より包括的）
    content = re.sub(pattern2, fix_pattern2, content, flags=re.DOTALL)
    
    if content != original_content:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Fixed {file}")
    else:
        print(f"- No changes needed for {file}")

print("\nDone!")
