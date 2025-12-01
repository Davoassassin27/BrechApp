import os
from pathlib import Path
import subprocess
import sys

def check_pandoc():
    try:
        result = subprocess.run(['pandoc', '--version'], 
                              capture_output=True, 
                              text=True)
        if result.returncode == 0:
            print("✓ Pandoc está instalado")
            print(f"  Versión: {result.stdout.split()[1]}")
            return True
    except FileNotFoundError:
        pass
    
    print("✗ Pandoc no está instalado")
    print("\nPara instalar Pandoc:")
    print("  Windows: choco install pandoc")
    print("           o descargar desde https://pandoc.org/installing.html")
    print("  Linux:   sudo apt-get install pandoc")
    print("  Mac:     brew install pandoc")
    return False

def convert_md_to_docx(input_file, output_file=None):
    if not os.path.exists(input_file):
        print(f"✗ Error: El archivo {input_file} no existe")
        return False
    
    if output_file is None:
        output_file = input_file.replace('.md', '.docx')
    
    print(f"\n📄 Convirtiendo:")
    print(f"  Entrada:  {input_file}")
    print(f"  Salida:   {output_file}")
    
    try:
        cmd = [
            'pandoc',
            input_file,
            '-o', output_file,
            '--from=markdown',
            '--to=docx',
            '--reference-doc=reference.docx' if os.path.exists('reference.docx') else '',
            '--toc',
            '--toc-depth=3',
            '--number-sections',
            '--highlight-style=tango'
        ]
        
        cmd = [arg for arg in cmd if arg]
        
        result = subprocess.run(cmd, 
                              capture_output=True, 
                              text=True,
                              check=True)
        
        if os.path.exists(output_file):
            size = os.path.getsize(output_file) / 1024
            print(f"\n✓ Conversión exitosa!")
            print(f"  Archivo generado: {output_file}")
            print(f"  Tamaño: {size:.2f} KB")
            return True
        else:
            print(f"\n✗ Error: No se generó el archivo de salida")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error durante la conversión:")
        print(f"  {e.stderr}")
        return False
    except Exception as e:
        print(f"\n✗ Error inesperado: {e}")
        return False

def main():
    print("=" * 60)
    print("  Conversor Markdown → DOCX para BrechApp")
    print("=" * 60)
    
    if not check_pandoc():
        sys.exit(1)
    
    input_file = 'docs/Informe_BrechApp_MyS.md'
    output_file = 'docs/Informe_BrechApp_MyS.docx'
    
    if not os.path.exists('docs'):
        print("\n✗ Error: La carpeta 'docs' no existe")
        sys.exit(1)
    
    success = convert_md_to_docx(input_file, output_file)
    
    if success:
        print("\n" + "=" * 60)
        print("  ✓ Proceso completado exitosamente")
        print("=" * 60)
        print(f"\nPuedes abrir el documento con:")
        print(f"  start {output_file}  (Windows)")
        print(f"  open {output_file}   (Mac)")
        print(f"  xdg-open {output_file}  (Linux)")
    else:
        print("\n" + "=" * 60)
        print("  ✗ La conversión falló")
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()
