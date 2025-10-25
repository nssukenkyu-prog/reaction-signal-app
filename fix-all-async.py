import re
import os

files = [
    'app/page.tsx',
    'app/color/page.tsx',
    'app/simple/page.tsx',
    'app/sprint/page.tsx',
    'app/dual/page.tsx',
    'app/ranking/page.tsx'
]

def fix_file(filepath):
    if not os.path.exists(filepath):
        print(f"⚠ Skipping {filepath} (not found)")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # パターン1: app/page.tsx のuseEffect
    pattern1 = r'(useEffect\(\(\) => \{)\s*const user = getUser\(\);\s*setCurrentUser\(user\);'
    replacement1 = r'\1\n    const loadData = async () => {\n      const user = await getUser();\n      setCurrentUser(user);'
    
    if 'const user = getUser();' in content and 'setCurrentUser(user);' in content:
        # app/page.tsxの特殊なパターン
        content = re.sub(
            r'useEffect\(\(\) => \{\s*const user = getUser\(\);\s*setCurrentUser\(user\);\s*const sessionData = getCurrentSession\(\);\s*setSession\(sessionData\);\s*\}, \[\]\);',
            '''useEffect(() => {
    const loadData = async () => {
      const user = await getUser();
      setCurrentUser(user);
      
      const sessionData = await getCurrentSession();
      setSession(sessionData);
    };
    loadData();
  }, []);''',
            content
        )
    
    # パターン2: 他のページのuseEffect（getUser + router.push）
    if 'const currentUser = getUser();' in content:
        content = re.sub(
            r'useEffect\(\(\) => \{\s*const currentUser = getUser\(\);',
            '''useEffect(() => {
    const loadUser = async () => {
      const currentUser = await getUser();''',
            content
        )
        # 対応する閉じカッコを追加
        content = re.sub(
            r'(setUser\(currentUser\);)\s*(\}, \[router\]\);)',
            r'\1\n    };\n    loadUser();\n  }, [router]);',
            content
        )
    
    # パターン3: handleStart, handleComplete など
    # const handleXxx = () => { で始まり、内部にawaitがある場合
    content = re.sub(
        r'const (handle\w+) = \(\) => \{([^}]*await [^}]*)\}',
        r'const \1 = async () => {\2}',
        content,
        flags=re.DOTALL
    )
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Fixed {filepath}")
        return True
    else:
        print(f"- No changes needed for {filepath}")
        return False

print("Fixing async/await issues in all pages...\n")
fixed_count = 0
for file in files:
    if fix_file(file):
        fixed_count += 1

print(f"\n✓ Fixed {fixed_count} file(s)")
