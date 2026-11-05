import os

target_files = [
    'src/app/dashboard/page.tsx',
    'src/app/dashboard/custom-practice/page.tsx',
    'src/app/dashboard/exam/page.tsx',
    'src/app/dashboard/notebook/page.tsx',
    'src/app/dashboard/profile/page.tsx',
    'src/app/dashboard/revision/page.tsx',
    'src/app/dashboard/syllabus/page.tsx',
    'src/app/dashboard/syllabus/[subjectId]/page.tsx',
    'src/app/auth/login/page.tsx',
    'src/app/auth/register/page.tsx',
    'src/app/auth/forgot-password/page.tsx',
    'src/app/auth/reset-password/page.tsx'
]

base_dir = r'c:\VS Code\Codes\dgcacpllearning'
updated = 0
target_str = 'export const dynamic = "force-dynamic";'

for rel in target_files:
    full_path = os.path.join(base_dir, rel)
    if os.path.exists(full_path):
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if target_str in content:
            new_content = content.replace(target_str + '\n\n', '').replace(target_str + '\n', '').replace(target_str, '')
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updated += 1
            print(f'Optimized {rel}')

print(f'Successfully optimized {updated} pages for static edge delivery.')

