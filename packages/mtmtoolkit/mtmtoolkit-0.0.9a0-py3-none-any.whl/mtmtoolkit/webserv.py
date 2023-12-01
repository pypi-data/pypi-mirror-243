import os
from flask import Flask, render_template_string, request, jsonify


app = Flask(__name__, static_folder='temp')
temp_directory = 'temp'
if not os.path.exists(temp_directory):
        os.makedirs(temp_directory)

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
print("Current working directory:", os.getcwd())

@app.route('/pass_pdb', methods=['POST'])
def pass_pdb():
    pdb_data = request.form['pdb']
    with open('temp/molecule.pdb', 'w') as file:
        file.write(pdb_data)
    return jsonify({'status': 'PDB data received'})


@app.route('/visualize_molecule')
def visualize_molecule():
    html_content = '''
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://3Dmol.org/build/3Dmol-min.js"></script>
    <script src="https://3Dmol.org/build/3Dmol.ui-min.js"></script>

    <div id="pdbViewer" style="height: 100vh; width: 100vw; overflow: hidden;"></div>

    <script>
        var viewer = $3Dmol.createViewer("pdbViewer", { backgroundColor: "0xffffff" });
        
        // Load the PDB file from the temp directory
        $.get('/temp/molecule.pdb', function(data) {
            viewer.addModel(data, "pdb");
            viewer.setStyle({ stick: {} });
            viewer.zoomTo();
            viewer.render();
        });
    </script>
    '''
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(debug=False)
    







