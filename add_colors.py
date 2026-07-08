import glob

def add_colors():
    target_dir = 'web/src'
    files = glob.glob(f'{target_dir}/**/*.tsx', recursive=True)
    files.append('web/src/app/globals.css')
    
    replacements = {
        # Soften main text
        'text-black': 'text-slate-800',
        # Soften borders
        'border-black': 'border-slate-200',
        'border-2 border-slate-200': 'border border-slate-200',
        # Primary buttons/accents (black background -> beautiful modern blue gradient or solid blue)
        'bg-black': 'bg-blue-600',
        'hover:bg-gray-800': 'hover:bg-blue-700',
        'hover:bg-gray-100': 'hover:bg-slate-50',
        # Neobrutalist solid shadows to modern soft shadows
        'shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]': 'shadow-lg shadow-blue-900/5',
        'shadow-[6px_6px_0px_0px_rgba(0,0,0,1)]': 'shadow-xl shadow-blue-900/10',
        'shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]': 'shadow-2xl shadow-blue-900/10',
        # Text colors for metrics and specific accents
        'text-blue-600/50': 'text-slate-500', # if bg-black text-white/50 was converted
        # Typography adjustments
        'font-black': 'font-extrabold',
    }
    
    for filepath in files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        
        for old, new in replacements.items():
            content = content.replace(old, new)
            
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Added colors to: {filepath}")

if __name__ == '__main__':
    add_colors()
