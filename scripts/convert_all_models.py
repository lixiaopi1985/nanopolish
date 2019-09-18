

import sys
import os.path
import os

functions = list()
outfiles = list()

for model_file in sys.stdin:
    model_file = model_file.rstrip()
    basename = os.path.basename(model_file).replace(".", "_")
    outfile = "builtin_models/%s.inl" % basename
    function_name = "initialize_%s_builtin" % (basename)
    
    ret = os.system("python scripts/convert_model_to_header.py -i %s -f %s > src/%s" % (model_file, function_name, outfile))
    if ret != 0:
        sys.stderr.write("Error processing %s\n" % model_file)
        sys.exit(1)

    functions.append(function_name)
    outfiles.append(outfile)

print("// Autogenerated from convert_all_models.py")
for f in outfiles:
    print("#include \"%s\"" % f)

print("\n// Autogenerated from convert_all_models.py")
print("const static std::vector<PoreModel> builtin_models({")
print("\t" + ",\n\t".join([f + "()" for f in functions]))
print("});")

