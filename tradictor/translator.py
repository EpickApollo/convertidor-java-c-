# translator.py
import re
from typing import List

# ---------- utilidades ----------
def dedent_lines(code: str) -> List[str]:
    return [line.rstrip() for line in code.splitlines()]

# ---------- transformaciones básicas ----------
def translate_print_java_to_js(line: str) -> str:
    # System.out.println("x");
    return re.sub(r'System\.out\.println\s*\((.*)\)\s*;', r'console.log(\1);', line)

def translate_print_java_to_cpp(line: str) -> str:
    # System.out.println("x"); -> std::cout << "x" << std::endl;
    return re.sub(r'System\.out\.println\s*\((.*)\)\s*;', r'std::cout << \1 << std::endl;', line)

def translate_variable_decl_java_to_js(line: str) -> str:
    # int a = 5; double x; String s = "hi";
    line = line.strip()
    # String -> let (assume mutable), primitives -> let
    line = re.sub(r'\bString\b', '', line)
    line = re.sub(r'\bint\b|\bdouble\b|\bfloat\b|\bboolean\b|\blong\b', 'let', line)
    # remove excessive spaces
    line = re.sub(r'\s+', ' ', line)
    return line

def translate_variable_decl_java_to_cpp(line: str) -> str:
    # Java types mostly same in C++
    return line

def translate_method_signature_java_to_js(line: str) -> str:
    # public static void main(String[] args) -> function main(args) {
    m = re.match(r'\s*(public|private|protected)?\s*(static)?\s*(\w+)\s+(\w+)\s*\((.*)\)\s*{', line)
    if m:
        ret_type = m.group(3)
        name = m.group(4)
        args = m.group(5).strip()
        # convert args: "String[] args" -> "args"
        args = re.sub(r'\bString\[\]\s+(\w+)', r'\1', args)
        args = re.sub(r'\bString\s+(\w+)', r'\1', args)
        return f'function {name}({args})' + ' {'
    return line

def translate_method_signature_java_to_cpp(line: str) -> str:
    # Keep similar but remove access modifiers
    line = re.sub(r'\b(public|private|protected)\b\s*', '', line)
    return line

# ---------- high-level translator ----------
def translate_java_to_js(java_code: str) -> str:
    out_lines = []
    for line in java_code.splitlines():
        stripped = line.strip()
        if 'System.out.println' in line:
            out_lines.append(translate_print_java_to_js(line))
            continue
        if re.search(r'\b(public|private|protected).*{', line):
            out_lines.append(translate_method_signature_java_to_js(line))
            continue
        # variable declarations
        if re.match(r'\s*(int|double|float|boolean|String|long)\b', stripped):
            out_lines.append(translate_variable_decl_java_to_js(line))
            continue
        # class declaration -> in JS convert to class skeleton
        class_m = re.match(r'\s*public\s+class\s+(\w+)\s*{', line)
        if class_m:
            out_lines.append(f'class {class_m.group(1)}' + ' {')
            continue
        # simple replacements
        line2 = line
        line2 = line2.replace('boolean', '')  # we handled types above simplistically
        line2 = line2.replace('this.', 'this.')
        out_lines.append(line2)
    return '\n'.join(out_lines)

def translate_java_to_cpp(java_code: str) -> str:
    out_lines = []
    for line in java_code.splitlines():
        if 'System.out.println' in line:
            out_lines.append(translate_print_java_to_cpp(line))
            continue
        if re.search(r'\b(public|private|protected).*{', line):
            out_lines.append(translate_method_signature_java_to_cpp(line))
            continue
        out_lines.append(line)
    # add includes for cout if print used
    if 'std::cout' in '\n'.join(out_lines):
        header = ['#include <iostream>', 'using namespace std;', '']
        return '\n'.join(header + out_lines)
    return '\n'.join(out_lines)

# ---------- demo ----------
if __name__ == '__main__':
    sample_java = """\
public class HolaMundo {
    public static void main(String[] args) {
        int a = 5;
        String s = "hola";
        System.out.println("Hola " + s + " numero " + a);
    }
}
"""
    print("=== JAVA ===")
    print(sample_java)
    print("=== JS ===")
    print(translate_java_to_js(sample_java))
    print("=== C++ ===")
    print(translate_java_to_cpp(sample_java))
