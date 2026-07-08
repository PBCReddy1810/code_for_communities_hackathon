import os
import glob

def fix_colors():
    target_dir = 'web/src'
    files = glob.glob(f'{target_dir}/**/*.tsx', recursive=True)
    
    replacements = {
        'text-white/40': 'text-black',
        'text-white/50': 'text-black',
        'text-white/80': 'text-black',
        'text-black/30': 'text-black',
        'text-black/50': 'text-black',
        'text-white': 'text-black',
        'text-slate-100': 'text-black',
        'text-slate-200': 'text-black',
        'text-slate-300': 'text-black',
        'text-slate-400': 'text-black',
        'text-slate-500': 'text-black',
        'text-gray-400': 'text-black',
        'text-gray-500': 'text-black',
        'bg-black': 'bg-white',
        'bg-slate-800': 'bg-white',
        'bg-slate-900': 'bg-white',
        'bg-slate-950': 'bg-white',
        'border-white': 'border-black',
        'border-white/10': 'border-black',
        'border-white/20': 'border-black',
        'border-black/10': 'border-black'
    }
    
    for filepath in files:
        # Skip the ones we've already perfected manually
        if 'mp-dashboard' in filepath or 'not-found' in filepath or filepath.endswith('app\\page.tsx'):
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        
        for old, new in replacements.items():
            content = content.replace(old, new)
            
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed colors in: {filepath}")

if __name__ == '__main__':
    fix_colors()
