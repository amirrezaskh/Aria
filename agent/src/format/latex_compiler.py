import os
import subprocess


class LatexCompiler:

    @staticmethod
    def compile_latex(latex_code: str, output_dir: str, latex_filename: str):
        os.makedirs(output_dir, exist_ok=True)
        latex_filepath = os.path.join(output_dir, latex_filename)

        with open(latex_filepath, "w", encoding="utf-8") as f:
            f.write(latex_code)

        pdf_filepath = None
        try:
            # Change to output directory for compilation
            original_cwd = os.getcwd()
            os.chdir(output_dir)

            # Run pdflatex twice for proper references
            for _ in range(2):
                subprocess.run(["pdflatex", "-interaction=nonstopmode", latex_filename],
                               check=True, capture_output=True, text=True)

            # Clean up auxiliary files
            base_name = os.path.splitext(latex_filename)[0]
            aux_extensions = ['.aux', '.log', '.out', '.fdb_latexmk', '.fls']
            for ext in aux_extensions:
                aux_file = base_name + ext
                if os.path.exists(aux_file):
                    os.remove(aux_file)

            pdf_filepath = os.path.join(output_dir, f"{base_name}.pdf")

        except subprocess.CalledProcessError as e:
            print(f"LaTeX compilation failed: {e}")
            print(f"Error output: {e.stderr}")
        except FileNotFoundError:
            print("pdflatex not found. Please install LaTeX (e.g., MacTeX on macOS)")
        finally:
            # Return to original directory
            os.chdir(original_cwd)

        return {
            "latex_file": latex_filepath,
            "pdf_file": pdf_filepath if pdf_filepath and os.path.exists(pdf_filepath) else None
        }
