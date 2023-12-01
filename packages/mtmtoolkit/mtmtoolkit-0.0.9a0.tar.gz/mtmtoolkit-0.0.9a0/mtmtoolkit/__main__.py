
import os
import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLabel, QLineEdit, QFileDialog, QGridLayout, QComboBox, QCompleter, QTabWidget, QVBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt6.QtCore import QByteArray, QUrl
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import Draw
import atexit

# common functions

# common functions

def cleanup_file():
    file_path = 'temp/molecule.pdb'
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Deleted file: {file_path}")

def smiles_to_xyz(smiles_string):
    mol = Chem.MolFromSmiles(smiles_string)
    if mol is None:
        return None, 0, 0  # Return None to indicate that the conversion failed

    mol = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol, AllChem.ETKDG())
    AllChem.MMFFOptimizeMolecule(mol)

    charge = Chem.GetFormalCharge(mol)
    num_radicals = Descriptors.NumRadicalElectrons(mol)
    multiplicity = num_radicals + 1 

    xyz_str = ""
    for atom in mol.GetAtoms():
        pos = mol.GetConformer().GetAtomPosition(atom.GetIdx())
        xyz_str += "{}\t{}\t{}\t{}\n".format(atom.GetSymbol(), pos.x, pos.y, pos.z)

    return xyz_str, charge, multiplicity

def smiles_to_pdb(smiles_string):
    mol = Chem.MolFromSmiles(smiles_string)
    if mol is None:
        return None

    mol = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol, AllChem.ETKDG())
    AllChem.MMFFOptimizeMolecule(mol)

    pdb_str = Chem.MolToPDBBlock(mol)
    return pdb_str

def pdb_to_xyz_data(pdb_file):
        # Read the PDB file
        mol = Chem.MolFromPDBFile(pdb_file, removeHs=False, sanitize=False)
        if mol is None:
            return None, None, None
        # Add hydrogens
        mol = Chem.AddHs(mol)
        
        # Get charge and multiplicity 
        charge = Chem.GetFormalCharge(mol)
        num_radicals = Descriptors.NumRadicalElectrons(mol)
        multiplicity = num_radicals + 1
        # Convert to XYZ format
        xyz_str = ""
        for atom in mol.GetAtoms():
            pos = mol.GetConformer().GetAtomPosition(atom.GetIdx())
            xyz_str += "{}\t{}\t{}\t{}\n".format(atom.GetSymbol(), pos.x, pos.y, pos.z)

        return xyz_str, charge, multiplicity

def file_exists_in_subdir(subdirectory, filename):
        file_path = os.path.join(subdirectory, filename)
        return os.path.exists(file_path)

def start_flask_app():
    global flask_process
    flask_process = subprocess.Popen(["python", "webserv.py"])
    print('Launching Server')

def stop_flask_app():
    if flask_process:
        flask_process.terminate()  # Send a terminate signal to the subprocess
        flask_process.wait() 
         

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
print("Current working directory:", os.getcwd())

# global constants
THEORIES = ["M06-2X", "CAM-B3LYP", "B3LYP", "HF"]
BASIS_SETS = ["6-31G(d,p)", "LanL2MB", "LanL2DZ", "6-31G", "6-31G(d)", "6-311G", "6-311++G(3df,3pd)", "cc-pVDZ", "cc-pVTZ"]
METHODS = ['opt', 'opt=tight', 'td=(root=1,nstates=30,noneqsolv)']
SOLVENTS = ['water', 'n-octanol', 'dichloromethane']
SOLVENT_METHODS = ['pcm', 'smd']


# controller
class GaussianInputController:
    def __init__(self, view):
        self.view = view
        self.main_window = MainWindow

    def generate_gaussian_input(self):

        # Retrieve data from the UI
        name = self.view.name_entry.text()
        smiles_string = self.view.smiles_entry.text()
        mem = self.view.memory_entry.text()
        nproc = self.view.nproc_entry.text()
        method = self.view.method_combo.currentText()
        basis = self.view.basis_combo.currentText()
        solvent = self.view.solvent_combo.currentText()
        solvent_method = self.view.solvent_method_combo.currentText()
        theory = self.view.theory_combo.currentText()
        other = self.view.other_entry.text()

        solvent_suffix = f"{solvent}{solvent_method}" if solvent and solvent_method else "vac"

        # Use the controller's logic to transform the SMILES string
        if file_exists_in_subdir('temp', 'molecule.pdb'):
            xyz_data, charge, multiplicity = pdb_to_xyz_data('temp/molecule.pdb')
            if xyz_data is None:
                self.view.result_label.setText("Error - Unable to process 'molecule.pdb'.")
                return
        else:
            xyz_data, charge, multiplicity = smiles_to_xyz(smiles_string)

        # Construct the Gaussian input file content
        input_string = f"%chk={name}_{method}_{theory}_{basis}_{solvent_suffix}.chk\n"
        input_string += f"%mem={mem}\n"
        input_string += f"%nproc={nproc}\n"
        
        scrf_string = ""
        if solvent and solvent_method:
            scrf_string = f"scrf=({solvent_method},solvent={solvent})"

        input_string += f"# {method} {theory}/{basis} {'symmetry=centerofmass'} {scrf_string} {other}\n\n"
        input_string += f"{name}_{method}_{theory}_{basis}_{solvent_suffix}\n\n"
        input_string += f"{charge} {multiplicity}\n"
        input_string += xyz_data + "\n"

        default_filename =  f"{name}_{method}_{theory}_{basis}_{solvent_suffix}.gjf"


        return input_string, default_filename


    def generate_and_save(self):
    # inputs needed for error checking
        name = self.view.name_entry.text().strip()
        smiles_string = self.view.smiles_entry.text().strip()
        solvent = self.view.solvent_combo.currentText().strip()
        solvent_method = self.view.solvent_method_combo.currentText().strip()
    
    # error - no name or SMILES string
        if not name or not smiles_string:
            error_message = "Please ensure all fields are filled out correctly."
            if not name:
                error_message = "Error - Molecule name required."
            elif not smiles_string:
                error_message = "Error - SMILES string required."

            self.view.result_label.setText(error_message)
            return  # Stop execution if there's an error

        xyz_data, charge, multiplicity = smiles_to_xyz(smiles_string)

    # error - invalid smiles string
        if xyz_data is None:
            self.view.result_label.setText("Error - The SMILES string is invalid. Please enter a valid SMILES string.")
            return  # Stop execution if there's an error

    # error - missing solvent or solvent method
        if bool(solvent) != bool(solvent_method):  # The condition here was incorrect, corrected it to check both
            self.view.result_label.setText("Error - both solvent and solvent method required.")
            return  # Stop execution if there's an error

    # Generate the input file string and default filename
        gaussian_input, default_filename = self.generate_gaussian_input()

    # Trigger save file dialog and save the file
        self.view.save_file_dialog(gaussian_input, default_filename)




# view
class MolViewer(QWidget):
    def __init__(self, mol=None):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.image_label = QLabel(self)
        self.layout.addWidget(self.image_label)
        if mol:
            self.updateMolView(mol)
    
 
    def updateMolView(self, mol):
        # Specify the desired image size (width, height)
        img_size = (575, 400)  # Adjust these values as needed

        # Generate a 2D depiction of the molecule with the specified size
        img = Draw.MolToImage(mol, size=img_size)

        # Save the image to a file (you can also use a BytesIO object)
        img_path = 'molecule.png'
        img.save(img_path)

        # Update the QPixmap with the new image
        pixmap = QPixmap(img_path)
        self.image_label.setPixmap(pixmap)


class ViewerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(400, 400, 400, 400)
        self.setWindowTitle('3D Molecule Viewer')
        layout = QVBoxLayout(self)
        self.smilesString = ""

        self.convertButton = QPushButton('Optimize Geometry', self)
        self.convertButton.clicked.connect(self.convertAndSendSmiles)
        layout.addWidget(self.convertButton)

        # QWebEngineView to display the visualization
        self.webView = QWebEngineView(self)
        layout.addWidget(self.webView)

        
    def setSmilesString(self, smiles):
        self.smilesString = smiles
    

    def convertAndSendSmiles(self):
        pdb_data = smiles_to_pdb(self.smilesString)
        if pdb_data:
            network_manager = QNetworkAccessManager(self)
            
            # Connect the finished signal to the onRequestFinished method
            network_manager.finished.connect(self.onRequestFinished)

            request = QNetworkRequest(QUrl('http://127.0.0.1:5000/pass_pdb'))
            request.setRawHeader(b"Content-Type", b"application/x-www-form-urlencoded")
            post_data = QByteArray()
            post_data.append(f"pdb={pdb_data}".encode('utf-8'))
            network_manager.post(request, post_data)
        else:
            print("Invalid SMILES string or conversion failed.")

    def onRequestFinished(self, reply):
        if reply.error() == QNetworkReply.NetworkError.NoError:
            self.webView.setUrl(QUrl('http://127.0.0.1:5000/visualize_molecule'))
        else:
            print("Error occurred:", reply.error())
    



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = GaussianInputController(self)
        self.setWindowTitle('MTMToolkit')
        self.setGeometry(100, 100, 600, 450)
        self.initializeUI()
       

    def initializeUI(self):
        # Create tab central widget
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
    
        # Define tabs
        self.tab1 = QWidget()
    

        # Add tabs
        self.tab_widget.addTab(self.tab1, "File Generation")
    

        # Add tab layouts
        tab1_grid_layout = QGridLayout(self.tab1)
    

        # Add widgets to "main" tab
        tab1_grid_layout.addWidget(QLabel("Enter Molecule Name:"), 0, 0)
        self.name_entry = QLineEdit()
        tab1_grid_layout.addWidget(self.name_entry, 0, 1)
        
        tab1_grid_layout.addWidget(QLabel("Enter SMILES:"), 1, 0)
        self.smiles_entry = QLineEdit()
        tab1_grid_layout.addWidget(self.smiles_entry, 1, 1)
        
        tab1_grid_layout.addWidget(QLabel("Memory:"), 2, 0)
        self.memory_entry = QLineEdit()
        self.memory_entry.setText('30GB')
        tab1_grid_layout.addWidget(self.memory_entry, 2, 1)
        
        tab1_grid_layout.addWidget(QLabel("nproc:"), 3, 0)
        self.nproc_entry = QLineEdit()
        self.nproc_entry.setText('48')
        tab1_grid_layout.addWidget(self.nproc_entry, 3, 1)

        tab1_grid_layout.addWidget(QLabel("Method:"), 4, 0)
        self.method_combo = QComboBox()
        self.method_combo.addItems(METHODS)
        self.method_combo.setEditable(True)
        method_completer = QCompleter(METHODS)
        method_completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.method_combo.setCompleter(method_completer)
        tab1_grid_layout.addWidget(self.method_combo, 4, 1)
        
        tab1_grid_layout.addWidget(QLabel("Solvent:"), 5, 0)
        self.solvent_combo = QComboBox()
        self.solvent_combo.addItems(SOLVENTS)
        self.solvent_combo.insertItem(0, "")  # Insert blank item at the start
        self.solvent_combo.setCurrentIndex(0)
        self.solvent_combo.setEditable(True)
        solvent_completer = QCompleter(SOLVENTS)
        solvent_completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.solvent_combo.setCompleter(solvent_completer)
        tab1_grid_layout.addWidget(self.solvent_combo, 5, 1)
        
        tab1_grid_layout.addWidget(QLabel("Solvent Method:"), 6, 0)
        self.solvent_method_combo = QComboBox()
        self.solvent_method_combo.addItems(SOLVENT_METHODS)
        self.solvent_method_combo.insertItem(0, "")  # Insert blank item at the start
        self.solvent_method_combo.setCurrentIndex(0)
        self.solvent_method_combo.setEditable(True)
        solvent_method_completer = QCompleter(SOLVENT_METHODS)
        solvent_method_completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.solvent_method_combo.setCompleter(solvent_method_completer)
        tab1_grid_layout.addWidget(self.solvent_method_combo, 6, 1)
        
        tab1_grid_layout.addWidget(QLabel("Theory:"), 7, 0)
        self.theory_combo = QComboBox()
        self.theory_combo.addItems(THEORIES)
        self.theory_combo.setEditable(True)
        theory_completer = QCompleter(THEORIES)
        theory_completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.theory_combo.setCompleter(theory_completer)
        tab1_grid_layout.addWidget(self.theory_combo, 7, 1)
        
        tab1_grid_layout.addWidget(QLabel("Basis:"), 8, 0)
        self.basis_combo = QComboBox()
        self.basis_combo.addItems(BASIS_SETS)
        self.basis_combo.setEditable(True)
        basis_completer = QCompleter(BASIS_SETS)
        basis_completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.basis_combo.setCompleter(basis_completer)
        tab1_grid_layout.addWidget(self.basis_combo, 8, 1)
        
        tab1_grid_layout.addWidget(QLabel("Other:"), 9, 0)
        self.other_entry = QLineEdit()
        tab1_grid_layout.addWidget(self.other_entry, 9, 1)
        
        self.generate_button = QPushButton("Generate and Save Input File")
        tab1_grid_layout.addWidget(self.generate_button, 11, 0, 1, 2)
        self.openViewerBtn = QPushButton('Generate 3D Model')
        tab1_grid_layout.addWidget(self.openViewerBtn, 12, 0, 1, 2)
        self.openViewerBtn.clicked.connect(self.openViewer)
        
        self.result_label = QLabel("")
        self.result_label.setWordWrap(True)
        tab1_grid_layout.addWidget(self.result_label, 13, 0, 1, 2)

        self.generate_button.clicked.connect(self.controller.generate_and_save)

    
      
    def openViewer(self):
        # Check if the viewer is already added to avoid multiple additions
        if hasattr(self, 'viewerWindow'):
            self.viewerWindow.close()

        # Placeholder for the 3D Viewer
        self.viewerWindow = ViewerWindow()
        self.originalSize = self.size()
    
        smiles_string = self.smiles_entry.text()
        if not smiles_string:
            error_message = 'Error - SMILES string required'
            self.result_label.setText(error_message)
            return 
        
        self.result_label.setText('')  # Clear any previous error message
        self.viewerWindow.setSmilesString(smiles_string)
        # Add Viewer to the Grid Layout
        tab1_grid_layout = self.tab1.layout()
        tab1_grid_layout.addWidget(self.viewerWindow, 0, 2, 15, 15) 

        # Adjust the stretch factors
        tab1_grid_layout.setColumnStretch(2, 3) 
        self.setGeometry(100, 100, 800, 450)
        self.viewerWindow.convertAndSendSmiles()


    def save_file_dialog(self, text, default_file_name):
        options = QFileDialog.Option.DontUseNativeDialog  
        filename, _ = QFileDialog.getSaveFileName(self, 
                                              "Save File", 
                                              default_file_name,  
                                              "Gaussian Input Files (*.gjf);;All Files (*)", 
                                              options=options)
        if filename:
            with open(filename, 'w') as f:
                f.write(text)


# main
def main():
    start_flask_app()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    atexit.register(stop_flask_app,)
    atexit.register(cleanup_file)
    sys.exit(app.exec())
    

if __name__ == "__main__":
    main()