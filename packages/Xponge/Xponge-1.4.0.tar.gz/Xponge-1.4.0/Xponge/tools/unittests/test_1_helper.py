"""
    This **module** includes unittests of the basic functions of Xponge.helper
"""

__all__ = ["test_adding_of_residues",
           "test_omitting_residue_type",
           "test_reseting_type",
           "test_pdb_filter"]

def test_adding_of_residues():
    """
        test adding and multiplying of Xponge.ResidueType and Xponge.Moleule
    """
    import Xponge
    import Xponge.forcefield.amber.ff14sb
    globals().update(Xponge.ResidueType.get_all_types())

    t1 = ACE + ALA + NME
    assert len(t1.residues) == 3
    assert len(t1.residue_links) == 2
    t2 = ALA * 3
    assert len(t2.residues) == 3
    assert len(t2.residue_links) == 2
    t3 = t2 + t1
    assert len(t3.residues) == 6
    assert len(t3.residue_links) == 4
    assert len(t2.residues) == 3
    assert len(t2.residue_links) == 2
    assert len(t1.residues) == 3
    assert len(t1.residue_links) == 2
    t4 = t2 * 3
    assert len(t4.residues) == 9
    assert len(t4.residue_links) == 8
    assert len(t2.residues) == 3
    assert len(t2.residue_links) == 2
    t5 = ACE | ALA | NME
    assert len(t5.residues) == 3
    assert len(t5.residue_links) == 0

def test_omitting_residue_type():
    """
        test omitting atoms for a residue type
    """
    import Xponge
    import Xponge.forcefield.amber.ff14sb
    globals().update(Xponge.ResidueType.get_all_types())

    blb = ALA.deepcopy("BLB")
    blb.omit_atoms("O", charge=+2)
    assert int(round(blb.charge)) == 2 and abs(blb.charge - 2) < 0.001

def test_reseting_type():
    """
        test change the type of certain residue
    """
    import Xponge
    import Xponge.forcefield.amber.ff14sb
    globals().update(Xponge.ResidueType.get_all_types())

    mol = ALA * 10
    mol.residues[0].set_type("NGLY", add_missing_atoms=True)
    assert mol.residues[0].name == "NGLY"
    mol.residues[0].unterminal()
    assert mol.residues[0].name == "GLY"

def test_pdb_filter():
    """
        test the pdb filter
    """
    import Xponge
    from io import StringIO
    s_in = StringIO(r"""
HEADER    TRANSCRIPTION/DNA                       28-SEP-95   2DGC              
TITLE     GCN4 BASIC DOMAIN, LEUCINE ZIPPER COMPLEXED WITH ATF/CREB             
TITLE    2 SITE DNA                                                             
COMPND    MOL_ID: 1;                                                            
COMPND   2 MOLECULE: DNA (5'-                                                   
COMPND   3 D(*TP*GP*GP*AP*GP*AP*TP*GP*AP*CP*GP*TP*CP*AP*TP*CP*T                 
COMPND   4 P*CP*C)-3');                                                         
COMPND   5 CHAIN: B;                                                            
COMPND   6 ENGINEERED: YES;                                                     
COMPND   7 MOL_ID: 2;                                                           
COMPND   8 MOLECULE: PROTEIN (GCN4);                                            
COMPND   9 CHAIN: A                                                             
SOURCE    MOL_ID: 1;                                                            
SOURCE   2 SYNTHETIC: YES;                                                      
SOURCE   3 MOL_ID: 2;                                                           
SOURCE   4 ORGANISM_SCIENTIFIC: SACCHAROMYCES CEREVISIAE;                       
SOURCE   5 ORGANISM_COMMON: BAKER'S YEAST;                                      
SOURCE   6 ORGANISM_TAXID: 4932                                                 
KEYWDS    BASIC DOMAIN, LEUCINE ZIPPER, DNA BINDING, EUKARYOTIC                 
KEYWDS   2 REGULATORY PROTEIN, TRANSCRIPTION/DNA COMPLEX                        
EXPDTA    X-RAY DIFFRACTION                                                     
AUTHOR    W.KELLER,P.KOENIG,T.J.RICHMOND                                        
REVDAT   3   24-FEB-09 2DGC    1       VERSN                                    
REVDAT   2   01-APR-03 2DGC    1       JRNL                                     
REVDAT   1   08-MAR-96 2DGC    0                                                
JRNL        AUTH   W.KELLER,P.KONIG,T.J.RICHMOND                                
JRNL        TITL   CRYSTAL STRUCTURE OF A BZIP/DNA COMPLEX AT 2.2 A:            
JRNL        TITL 2 DETERMINANTS OF DNA SPECIFIC RECOGNITION.                    
JRNL        REF    J.MOL.BIOL.                   V. 254   657 1995              
JRNL        REFN                   ISSN 0022-2836                               
JRNL        PMID   7500340                                                      
JRNL        DOI    10.1006/JMBI.1995.0645                                       
REMARK   1                                                                      
REMARK   1 REFERENCE 1                                                          
REMARK   1  AUTH   P.KOENIG,T.J.RICHMOND                                        
REMARK   1  TITL   THE X-RAY STRUCTURE OF THE GCN4-BZIP BOUND TO                
REMARK   1  TITL 2 ATF/CREB SITE DNA SHOWS THE COMPLEX DEPENDS ON DNA           
REMARK   1  TITL 3 FLEXIBILITY                                                  
REMARK   1  REF    J.MOL.BIOL.                   V. 233   139 1993              
REMARK   1  REFN                   ISSN 0022-2836                               
REMARK   1 REFERENCE 2                                                          
REMARK   1  AUTH   T.E.ELLENBERGER,C.J.BRANDL,K.STRUHL,S.C.HARRISON             
REMARK   1  TITL   THE GCN4 BASIC REGION LEUCINE ZIPPER BINDS DNA AS            
REMARK   1  TITL 2 A DIMER OF UNINTERRUPTED ALPHA HELICES: CRYSTAL              
REMARK   1  TITL 3 STRUCTURE OF THE PROTEIN-DNA COMPLEX                         
REMARK   1  REF    CELL(CAMBRIDGE,MASS.)         V.  71  1223 1992              
REMARK   1  REFN                   ISSN 0092-8674                               
REMARK   2                                                                      
REMARK   2 RESOLUTION.    2.20 ANGSTROMS.                                       
REMARK   3                                                                      
REMARK   3 REFINEMENT.                                                          
REMARK   3   PROGRAM     : X-PLOR                                               
REMARK   3   AUTHORS     : BRUNGER                                              
REMARK   3                                                                      
REMARK   3  DATA USED IN REFINEMENT.                                            
REMARK   3   RESOLUTION RANGE HIGH (ANGSTROMS) : 2.20                           
REMARK   3   RESOLUTION RANGE LOW  (ANGSTROMS) : 6.00                           
REMARK   3   DATA CUTOFF            (SIGMA(F)) : 3.000                          
REMARK   3   DATA CUTOFF HIGH         (ABS(F)) : NULL                           
REMARK   3   DATA CUTOFF LOW          (ABS(F)) : NULL                           
REMARK   3   COMPLETENESS (WORKING+TEST)   (%) : 80.7                           
REMARK   3   NUMBER OF REFLECTIONS             : 5576                           
REMARK   3                                                                      
REMARK   3  FIT TO DATA USED IN REFINEMENT.                                     
REMARK   3   CROSS-VALIDATION METHOD          : NULL                            
REMARK   3   FREE R VALUE TEST SET SELECTION  : NULL                            
REMARK   3   R VALUE            (WORKING SET) : 0.214                           
REMARK   3   FREE R VALUE                     : 0.316                           
REMARK   3   FREE R VALUE TEST SET SIZE   (%) : NULL                            
REMARK   3   FREE R VALUE TEST SET COUNT      : NULL                            
REMARK   3   ESTIMATED ERROR OF FREE R VALUE  : NULL                            
REMARK   3                                                                      
REMARK   3  FIT IN THE HIGHEST RESOLUTION BIN.                                  
REMARK   3   TOTAL NUMBER OF BINS USED           : NULL                         
REMARK   3   BIN RESOLUTION RANGE HIGH       (A) : NULL                         
REMARK   3   BIN RESOLUTION RANGE LOW        (A) : NULL                         
REMARK   3   BIN COMPLETENESS (WORKING+TEST) (%) : NULL                         
REMARK   3   REFLECTIONS IN BIN    (WORKING SET) : NULL                         
REMARK   3   BIN R VALUE           (WORKING SET) : NULL                         
REMARK   3   BIN FREE R VALUE                    : NULL                         
REMARK   3   BIN FREE R VALUE TEST SET SIZE  (%) : NULL                         
REMARK   3   BIN FREE R VALUE TEST SET COUNT     : NULL                         
REMARK   3   ESTIMATED ERROR OF BIN FREE R VALUE : NULL                         
REMARK   3                                                                      
REMARK   3  NUMBER OF NON-HYDROGEN ATOMS USED IN REFINEMENT.                    
REMARK   3   PROTEIN ATOMS            : 427                                     
REMARK   3   NUCLEIC ACID ATOMS       : 386                                     
REMARK   3   HETEROGEN ATOMS          : 0                                       
REMARK   3   SOLVENT ATOMS            : 46                                      
REMARK   3                                                                      
REMARK   3  B VALUES.                                                           
REMARK   3   FROM WILSON PLOT           (A**2) : NULL                           
REMARK   3   MEAN B VALUE      (OVERALL, A**2) : 41.30                          
REMARK   3   OVERALL ANISOTROPIC B VALUE.                                       
REMARK   3    B11 (A**2) : NULL                                                 
REMARK   3    B22 (A**2) : NULL                                                 
REMARK   3    B33 (A**2) : NULL                                                 
REMARK   3    B12 (A**2) : NULL                                                 
REMARK   3    B13 (A**2) : NULL                                                 
REMARK   3    B23 (A**2) : NULL                                                 
REMARK   3                                                                      
REMARK   3  ESTIMATED COORDINATE ERROR.                                         
REMARK   3   ESD FROM LUZZATI PLOT        (A) : 0.32                            
REMARK   3   ESD FROM SIGMAA              (A) : NULL                            
REMARK   3   LOW RESOLUTION CUTOFF        (A) : NULL                            
REMARK   3                                                                      
REMARK   3  CROSS-VALIDATED ESTIMATED COORDINATE ERROR.                         
REMARK   3   ESD FROM C-V LUZZATI PLOT    (A) : NULL                            
REMARK   3   ESD FROM C-V SIGMAA          (A) : NULL                            
REMARK   3                                                                      
REMARK   3  RMS DEVIATIONS FROM IDEAL VALUES.                                   
REMARK   3   BOND LENGTHS                 (A) : NULL                            
REMARK   3   BOND ANGLES            (DEGREES) : NULL                            
REMARK   3   DIHEDRAL ANGLES        (DEGREES) : NULL                            
REMARK   3   IMPROPER ANGLES        (DEGREES) : NULL                            
REMARK   3                                                                      
REMARK   3  ISOTROPIC THERMAL MODEL : NULL                                      
REMARK   3                                                                      
REMARK   3  ISOTROPIC THERMAL FACTOR RESTRAINTS.    RMS    SIGMA                
REMARK   3   MAIN-CHAIN BOND              (A**2) : NULL  ; NULL                 
REMARK   3   MAIN-CHAIN ANGLE             (A**2) : NULL  ; NULL                 
REMARK   3   SIDE-CHAIN BOND              (A**2) : NULL  ; NULL                 
REMARK   3   SIDE-CHAIN ANGLE             (A**2) : NULL  ; NULL                 
REMARK   3                                                                      
REMARK   3  NCS MODEL : NULL                                                    
REMARK   3                                                                      
REMARK   3  NCS RESTRAINTS.                         RMS   SIGMA/WEIGHT          
REMARK   3   GROUP  1  POSITIONAL            (A) : NULL  ; NULL                 
REMARK   3   GROUP  1  B-FACTOR           (A**2) : NULL  ; NULL                 
REMARK   3                                                                      
REMARK   3  PARAMETER FILE  1  : PARAM11.DNA                                    
REMARK   3  PARAMETER FILE  2  : NULL                                           
REMARK   3  TOPOLOGY FILE  1   : NULL                                           
REMARK   3  TOPOLOGY FILE  2   : NULL                                           
REMARK   3                                                                      
REMARK   3  OTHER REFINEMENT REMARKS: NULL                                      
REMARK   4                                                                      
REMARK   4 2DGC COMPLIES WITH FORMAT V. 3.15, 01-DEC-08                         
REMARK 100                                                                      
REMARK 100 THIS ENTRY HAS BEEN PROCESSED BY BNL.                                
REMARK 200                                                                      
REMARK 200 EXPERIMENTAL DETAILS                                                 
REMARK 200  EXPERIMENT TYPE                : X-RAY DIFFRACTION                  
REMARK 200  DATE OF DATA COLLECTION        : NULL                               
REMARK 200  TEMPERATURE           (KELVIN) : 277.00                             
REMARK 200  PH                             : 4.60                               
REMARK 200  NUMBER OF CRYSTALS USED        : 1                                  
REMARK 200                                                                      
REMARK 200  SYNCHROTRON              (Y/N) : Y                                  
REMARK 200  RADIATION SOURCE               : EMBL/DESY, HAMBURG                 
REMARK 200  BEAMLINE                       : X11                                
REMARK 200  X-RAY GENERATOR MODEL          : NULL                               
REMARK 200  MONOCHROMATIC OR LAUE    (M/L) : M                                  
REMARK 200  WAVELENGTH OR RANGE        (A) : 0.92                               
REMARK 200  MONOCHROMATOR                  : NULL                               
REMARK 200  OPTICS                         : NULL                               
REMARK 200                                                                      
REMARK 200  DETECTOR TYPE                  : IMAGE PLATE                        
REMARK 200  DETECTOR MANUFACTURER          : MARRESEARCH                        
REMARK 200  INTENSITY-INTEGRATION SOFTWARE : OSCREF, OSCKRUNCH                  
REMARK 200  DATA SCALING SOFTWARE          : NULL                               
REMARK 200                                                                      
REMARK 200  NUMBER OF UNIQUE REFLECTIONS   : 6597                               
REMARK 200  RESOLUTION RANGE HIGH      (A) : 2.200                              
REMARK 200  RESOLUTION RANGE LOW       (A) : 15.000                             
REMARK 200  REJECTION CRITERIA  (SIGMA(I)) : NULL                               
REMARK 200                                                                      
REMARK 200 OVERALL.                                                             
REMARK 200  COMPLETENESS FOR RANGE     (%) : 80.8                               
REMARK 200  DATA REDUNDANCY                : 5.000                              
REMARK 200  R MERGE                    (I) : 0.09000                            
REMARK 200  R SYM                      (I) : NULL                               
REMARK 200  <I/SIGMA(I)> FOR THE DATA SET  : NULL                               
REMARK 200                                                                      
REMARK 200 IN THE HIGHEST RESOLUTION SHELL.                                     
REMARK 200  HIGHEST RESOLUTION SHELL, RANGE HIGH (A) : NULL                     
REMARK 200  HIGHEST RESOLUTION SHELL, RANGE LOW  (A) : NULL                     
REMARK 200  COMPLETENESS FOR SHELL     (%) : NULL                               
REMARK 200  DATA REDUNDANCY IN SHELL       : NULL                               
REMARK 200  R MERGE FOR SHELL          (I) : NULL                               
REMARK 200  R SYM FOR SHELL            (I) : NULL                               
REMARK 200  <I/SIGMA(I)> FOR SHELL         : NULL                               
REMARK 200                                                                      
REMARK 200 DIFFRACTION PROTOCOL: SINGLE WAVELENGTH                              
REMARK 200 METHOD USED TO DETERMINE THE STRUCTURE: NULL                         
REMARK 200 SOFTWARE USED: NULL                                                  
REMARK 200 STARTING MODEL: NULL                                                 
REMARK 200                                                                      
REMARK 200 REMARK: NULL                                                         
REMARK 280                                                                      
REMARK 280 CRYSTAL                                                              
REMARK 280 SOLVENT CONTENT, VS   (%): 55.82                                     
REMARK 280 MATTHEWS COEFFICIENT, VM (ANGSTROMS**3/DA): 2.78                     
REMARK 280                                                                      
REMARK 280 CRYSTALLIZATION CONDITIONS: PH 4.60, VAPOR DIFFUSION                 
REMARK 290                                                                      
REMARK 290 CRYSTALLOGRAPHIC SYMMETRY                                            
REMARK 290 SYMMETRY OPERATORS FOR SPACE GROUP: P 41 21 2                        
REMARK 290                                                                      
REMARK 290      SYMOP   SYMMETRY                                                
REMARK 290     NNNMMM   OPERATOR                                                
REMARK 290       1555   X,Y,Z                                                   
REMARK 290       2555   -X,-Y,Z+1/2                                             
REMARK 290       3555   -Y+1/2,X+1/2,Z+1/4                                      
REMARK 290       4555   Y+1/2,-X+1/2,Z+3/4                                      
REMARK 290       5555   -X+1/2,Y+1/2,-Z+1/4                                     
REMARK 290       6555   X+1/2,-Y+1/2,-Z+3/4                                     
REMARK 290       7555   Y,X,-Z                                                  
REMARK 290       8555   -Y,-X,-Z+1/2                                            
REMARK 290                                                                      
REMARK 290     WHERE NNN -> OPERATOR NUMBER                                     
REMARK 290           MMM -> TRANSLATION VECTOR                                  
REMARK 290                                                                      
REMARK 290 CRYSTALLOGRAPHIC SYMMETRY TRANSFORMATIONS                            
REMARK 290 THE FOLLOWING TRANSFORMATIONS OPERATE ON THE ATOM/HETATM             
REMARK 290 RECORDS IN THIS ENTRY TO PRODUCE CRYSTALLOGRAPHICALLY                
REMARK 290 RELATED MOLECULES.                                                   
REMARK 290   SMTRY1   1  1.000000  0.000000  0.000000        0.00000            
REMARK 290   SMTRY2   1  0.000000  1.000000  0.000000        0.00000            
REMARK 290   SMTRY3   1  0.000000  0.000000  1.000000        0.00000            
REMARK 290   SMTRY1   2 -1.000000  0.000000  0.000000        0.00000            
REMARK 290   SMTRY2   2  0.000000 -1.000000  0.000000        0.00000            
REMARK 290   SMTRY3   2  0.000000  0.000000  1.000000       43.44000            
REMARK 290   SMTRY1   3  0.000000 -1.000000  0.000000       29.33000            
REMARK 290   SMTRY2   3  1.000000  0.000000  0.000000       29.33000            
REMARK 290   SMTRY3   3  0.000000  0.000000  1.000000       21.72000            
REMARK 290   SMTRY1   4  0.000000  1.000000  0.000000       29.33000            
REMARK 290   SMTRY2   4 -1.000000  0.000000  0.000000       29.33000            
REMARK 290   SMTRY3   4  0.000000  0.000000  1.000000       65.16000            
REMARK 290   SMTRY1   5 -1.000000  0.000000  0.000000       29.33000            
REMARK 290   SMTRY2   5  0.000000  1.000000  0.000000       29.33000            
REMARK 290   SMTRY3   5  0.000000  0.000000 -1.000000       21.72000            
REMARK 290   SMTRY1   6  1.000000  0.000000  0.000000       29.33000            
REMARK 290   SMTRY2   6  0.000000 -1.000000  0.000000       29.33000            
REMARK 290   SMTRY3   6  0.000000  0.000000 -1.000000       65.16000            
REMARK 290   SMTRY1   7  0.000000  1.000000  0.000000        0.00000            
REMARK 290   SMTRY2   7  1.000000  0.000000  0.000000        0.00000            
REMARK 290   SMTRY3   7  0.000000  0.000000 -1.000000        0.00000            
REMARK 290   SMTRY1   8  0.000000 -1.000000  0.000000        0.00000            
REMARK 290   SMTRY2   8 -1.000000  0.000000  0.000000        0.00000            
REMARK 290   SMTRY3   8  0.000000  0.000000 -1.000000       43.44000            
REMARK 290                                                                      
REMARK 290 REMARK: NULL                                                         
REMARK 300                                                                      
REMARK 300 BIOMOLECULE: 1                                                       
REMARK 300 SEE REMARK 350 FOR THE AUTHOR PROVIDED AND/OR PROGRAM                
REMARK 300 GENERATED ASSEMBLY INFORMATION FOR THE STRUCTURE IN                  
REMARK 300 THIS ENTRY. THE REMARK MAY ALSO PROVIDE INFORMATION ON               
REMARK 300 BURIED SURFACE AREA.                                                 
REMARK 300 REMARK: THE ASYMMETRIC UNIT CONTAINS ONE HALF OF PROTEIN/DNA         
REMARK 300 COMPLEX PER ASYMMETRIC UNIT.                                         
REMARK 300                                                                      
REMARK 300 MOLECULAR DYAD AXIS OF PROTEIN DIMER AND PALINDROMIC HALF            
REMARK 300 SITES OF THE DNA COINCIDES WITH CRYSTALLOGRAPHIC TWO-FOLD            
REMARK 300 AXIS.  THE FULL PROTEIN/DNA COMPLEX CAN BE OBTAINED BY               
REMARK 300 APPLYING THE FOLLOWING TRANSFORMATION MATRIX AND                     
REMARK 300 TRANSLATION VECTOR TO THE COORDINATES X Y Z:                         
REMARK 300                                                                      
REMARK 300 SYMMETRY                                                             
REMARK 300  THE CRYSTALLOGRAPHIC SYMMETRY TRANSFORMATIONS PRESENTED             
REMARK 300  BELOW GENERATE THE SUBUNITS OF THE POLYMERIC MOLECULE.              
REMARK 300                                                                      
REMARK 300  APPLIED TO RESIDUES:  A   229 ..     277                            
REMARK 300  APPLIED TO RESIDUES:  B   -10 ..       9                            
REMARK 300  SYMMETRY1   1  0.000000 -1.000000  0.000000      117.32000          
REMARK 300  SYMMETRY2   1 -1.000000  0.000000  0.000000      117.32000          
REMARK 300  SYMMETRY3   1  0.000000  0.000000 -1.000000       43.44000          
REMARK 350                                                                      
REMARK 350 COORDINATES FOR A COMPLETE MULTIMER REPRESENTING THE KNOWN           
REMARK 350 BIOLOGICALLY SIGNIFICANT OLIGOMERIZATION STATE OF THE                
REMARK 350 MOLECULE CAN BE GENERATED BY APPLYING BIOMT TRANSFORMATIONS          
REMARK 350 GIVEN BELOW.  BOTH NON-CRYSTALLOGRAPHIC AND                          
REMARK 350 CRYSTALLOGRAPHIC OPERATIONS ARE GIVEN.                               
REMARK 350                                                                      
REMARK 350 BIOMOLECULE: 1                                                       
REMARK 350 AUTHOR DETERMINED BIOLOGICAL UNIT: TETRAMERIC                        
REMARK 350 APPLY THE FOLLOWING TO CHAINS: B, A                                  
REMARK 350   BIOMT1   1  1.000000  0.000000  0.000000        0.00000            
REMARK 350   BIOMT2   1  0.000000  1.000000  0.000000        0.00000            
REMARK 350   BIOMT3   1  0.000000  0.000000  1.000000        0.00000            
REMARK 350   BIOMT1   2  0.000000 -1.000000  0.000000      117.32000            
REMARK 350   BIOMT2   2 -1.000000  0.000000  0.000000      117.32000            
REMARK 350   BIOMT3   2  0.000000  0.000000 -1.000000       43.44000            
REMARK 465                                                                      
REMARK 465 MISSING RESIDUES                                                     
REMARK 465 THE FOLLOWING RESIDUES WERE NOT LOCATED IN THE                       
REMARK 465 EXPERIMENT. (M=MODEL NUMBER; RES=RESIDUE NAME; C=CHAIN               
REMARK 465 IDENTIFIER; SSSEQ=SEQUENCE NUMBER; I=INSERTION CODE.)                
REMARK 465                                                                      
REMARK 465   M RES C SSSEQI                                                     
REMARK 465     MET A   219                                                      
REMARK 465     ILE A   220                                                      
REMARK 465     VAL A   221                                                      
REMARK 465     PRO A   222                                                      
REMARK 465     GLU A   223                                                      
REMARK 465     SER A   224                                                      
REMARK 465     SER A   225                                                      
REMARK 465     ASP A   226                                                      
REMARK 465     PRO A   227                                                      
REMARK 465     ALA A   228                                                      
REMARK 465     VAL A   278                                                      
REMARK 465     GLY A   279                                                      
REMARK 465     GLU A   280                                                      
REMARK 465     ARG A   281                                                      
REMARK 470                                                                      
REMARK 470 MISSING ATOM                                                         
REMARK 470 THE FOLLOWING RESIDUES HAVE MISSING ATOMS(M=MODEL NUMBER;            
REMARK 470 RES=RESIDUE NAME; C=CHAIN IDENTIFIER; SSEQ=SEQUENCE NUMBER;          
REMARK 470 I=INSERTION CODE):                                                   
REMARK 470   M RES CSSEQI  ATOMS                                                
REMARK 470     LYS A 276    CG   CD   CE   NZ                                   
REMARK 470     LEU A 277    CG   CD1  CD2                                       
REMARK 500                                                                      
REMARK 500 GEOMETRY AND STEREOCHEMISTRY                                         
REMARK 500 SUBTOPIC: COVALENT BOND LENGTHS                                      
REMARK 500                                                                      
REMARK 500 THE STEREOCHEMICAL PARAMETERS OF THE FOLLOWING RESIDUES              
REMARK 500 HAVE VALUES WHICH DEVIATE FROM EXPECTED VALUES BY MORE               
REMARK 500 THAN 6*RMSD (M=MODEL NUMBER; RES=RESIDUE NAME; C=CHAIN               
REMARK 500 IDENTIFIER; SSEQ=SEQUENCE NUMBER; I=INSERTION CODE).                 
REMARK 500                                                                      
REMARK 500 STANDARD TABLE:                                                      
REMARK 500 FORMAT: (10X,I3,1X,2(A3,1X,A1,I4,A1,1X,A4,3X),1X,F6.3)               
REMARK 500                                                                      
REMARK 500 EXPECTED VALUES PROTEIN: ENGH AND HUBER, 1999                        
REMARK 500 EXPECTED VALUES NUCLEIC ACID: CLOWNEY ET AL 1996                     
REMARK 500                                                                      
REMARK 500  M RES CSSEQI ATM1   RES CSSEQI ATM2   DEVIATION                     
REMARK 500     DT B -10   C5'    DT B -10   C4'     0.058                       
REMARK 500     DT B -10   N1     DT B -10   C2      0.056                       
REMARK 500     DG B  -9   C5'    DG B  -9   C4'     0.058                       
REMARK 500     DG B  -9   C6     DG B  -9   N1     -0.045                       
REMARK 500     DG B  -8   P      DG B  -8   O5'     0.095                       
REMARK 500     DG B  -8   C5'    DG B  -8   C4'     0.058                       
REMARK 500     DA B  -2   N9     DA B  -2   C4      0.045                       
REMARK 500     DG B   1   C6     DG B   1   N1     -0.051                       
REMARK 500     DT B   2   C5     DT B   2   C7      0.064                       
REMARK 500     DC B   6   P      DC B   6   O5'     0.092                       
REMARK 500     DC B   6   O3'    DT B   7   P       0.117                       
REMARK 500     DC B   8   P      DC B   8   O5'     0.082                       
REMARK 500     DC B   9   P      DC B   9   O5'     0.089                       
REMARK 500                                                                      
REMARK 500 REMARK: NULL                                                         
REMARK 500                                                                      
REMARK 500 GEOMETRY AND STEREOCHEMISTRY                                         
REMARK 500 SUBTOPIC: COVALENT BOND ANGLES                                       
REMARK 500                                                                      
REMARK 500 THE STEREOCHEMICAL PARAMETERS OF THE FOLLOWING RESIDUES              
REMARK 500 HAVE VALUES WHICH DEVIATE FROM EXPECTED VALUES BY MORE               
REMARK 500 THAN 6*RMSD (M=MODEL NUMBER; RES=RESIDUE NAME; C=CHAIN               
REMARK 500 IDENTIFIER; SSEQ=SEQUENCE NUMBER; I=INSERTION CODE).                 
REMARK 500                                                                      
REMARK 500 STANDARD TABLE:                                                      
REMARK 500 FORMAT: (10X,I3,1X,A3,1X,A1,I4,A1,3(1X,A4,2X),12X,F5.1)              
REMARK 500                                                                      
REMARK 500 EXPECTED VALUES PROTEIN: ENGH AND HUBER, 1999                        
REMARK 500 EXPECTED VALUES NUCLEIC ACID: CLOWNEY ET AL 1996                     
REMARK 500                                                                      
REMARK 500  M RES CSSEQI ATM1   ATM2   ATM3                                     
REMARK 500     DT B -10   O4' -  C1' -  C2' ANGL. DEV. =  -6.9 DEGREES          
REMARK 500     DT B -10   O4' -  C1' -  N1  ANGL. DEV. =   9.7 DEGREES          
REMARK 500     DT B -10   C4  -  C5  -  C6  ANGL. DEV. =   4.1 DEGREES          
REMARK 500     DT B -10   N3  -  C2  -  O2  ANGL. DEV. =  -4.8 DEGREES          
REMARK 500     DG B  -9   O4' -  C1' -  N9  ANGL. DEV. =  -5.9 DEGREES          
REMARK 500     DG B  -8   O4' -  C1' -  N9  ANGL. DEV. =   5.2 DEGREES          
REMARK 500     DA B  -7   C5' -  C4' -  O4' ANGL. DEV. =   9.1 DEGREES          
REMARK 500     DA B  -7   O4' -  C1' -  C2' ANGL. DEV. =  -5.4 DEGREES          
REMARK 500     DA B  -5   C1' -  O4' -  C4' ANGL. DEV. =   5.5 DEGREES          
REMARK 500     DA B  -5   O4' -  C1' -  C2' ANGL. DEV. =  -6.1 DEGREES          
REMARK 500     DT B  -4   O4' -  C1' -  N1  ANGL. DEV. =   2.5 DEGREES          
REMARK 500     DG B  -3   O4' -  C4' -  C3' ANGL. DEV. =   5.0 DEGREES          
REMARK 500     DT B  -4   C3' -  O3' -  P   ANGL. DEV. =  12.5 DEGREES          
REMARK 500     DA B  -2   O4' -  C4' -  C3' ANGL. DEV. =   4.3 DEGREES          
REMARK 500     DG B  -3   C3' -  O3' -  P   ANGL. DEV. =  10.7 DEGREES          
REMARK 500     DC B  -1   O4' -  C1' -  N1  ANGL. DEV. =  -4.9 DEGREES          
REMARK 500     DA B  -2   C3' -  O3' -  P   ANGL. DEV. =   8.3 DEGREES          
REMARK 500     DT B   2   N1  -  C2  -  N3  ANGL. DEV. =   3.6 DEGREES          
REMARK 500     DT B   2   N3  -  C2  -  O2  ANGL. DEV. =  -4.7 DEGREES          
REMARK 500     DG B   1   C3' -  O3' -  P   ANGL. DEV. =  14.3 DEGREES          
REMARK 500     DC B   3   O4' -  C1' -  C2' ANGL. DEV. =  -6.1 DEGREES          
REMARK 500     DC B   3   O4' -  C1' -  N1  ANGL. DEV. =   3.5 DEGREES          
REMARK 500     DC B   3   N1  -  C2  -  O2  ANGL. DEV. =   5.4 DEGREES          
REMARK 500     DA B   4   O4' -  C1' -  N9  ANGL. DEV. =  -4.3 DEGREES          
REMARK 500     DT B   5   C5' -  C4' -  C3' ANGL. DEV. = -12.2 DEGREES          
REMARK 500     DT B   5   C5' -  C4' -  O4' ANGL. DEV. =   6.8 DEGREES          
REMARK 500     DT B   5   C1' -  O4' -  C4' ANGL. DEV. =  -7.1 DEGREES          
REMARK 500     DT B   5   C4  -  C5  -  C6  ANGL. DEV. =   4.0 DEGREES          
REMARK 500     DT B   5   C6  -  C5  -  C7  ANGL. DEV. =  -4.5 DEGREES          
REMARK 500     DA B   4   C3' -  O3' -  P   ANGL. DEV. =  10.9 DEGREES          
REMARK 500     DC B   6   O4' -  C1' -  C2' ANGL. DEV. =  -5.3 DEGREES          
REMARK 500     DC B   6   O4' -  C1' -  N1  ANGL. DEV. =   4.1 DEGREES          
REMARK 500     DC B   6   N1  -  C2  -  O2  ANGL. DEV. =   4.2 DEGREES          
REMARK 500     DT B   7   C5' -  C4' -  C3' ANGL. DEV. = -11.1 DEGREES          
REMARK 500     DT B   7   N3  -  C2  -  O2  ANGL. DEV. =  -5.4 DEGREES          
REMARK 500     DC B   8   O4' -  C1' -  N1  ANGL. DEV. =   4.4 DEGREES          
REMARK 500     DC B   8   N1  -  C2  -  O2  ANGL. DEV. =   4.7 DEGREES          
REMARK 500     DC B   8   N3  -  C2  -  O2  ANGL. DEV. =  -4.3 DEGREES          
REMARK 500     DC B   9   O4' -  C1' -  N1  ANGL. DEV. =   3.3 DEGREES          
REMARK 500     DC B   8   C3' -  O3' -  P   ANGL. DEV. =  10.3 DEGREES          
REMARK 500                                                                      
REMARK 500 REMARK: NULL                                                         
REMARK 525                                                                      
REMARK 525 SOLVENT                                                              
REMARK 525                                                                      
REMARK 525 THE SOLVENT MOLECULES HAVE CHAIN IDENTIFIERS THAT                    
REMARK 525 INDICATE THE POLYMER CHAIN WITH WHICH THEY ARE MOST                  
REMARK 525 CLOSELY ASSOCIATED. THE REMARK LISTS ALL THE SOLVENT                 
REMARK 525 MOLECULES WHICH ARE MORE THAN 5A AWAY FROM THE                       
REMARK 525 NEAREST POLYMER CHAIN (M = MODEL NUMBER;                             
REMARK 525 RES=RESIDUE NAME; C=CHAIN IDENTIFIER; SSEQ=SEQUENCE                  
REMARK 525 NUMBER; I=INSERTION CODE):                                           
REMARK 525                                                                      
REMARK 525  M RES CSSEQI                                                        
REMARK 525    HOH B  13        DISTANCE = 12.48 ANGSTROMS                       
REMARK 525    HOH B  16        DISTANCE =  5.63 ANGSTROMS                       
REMARK 900                                                                      
REMARK 900 RELATED ENTRIES                                                      
REMARK 900 RELATED ID: 1DGC   RELATED DB: PDB                                   
REMARK 900 2DGC IS A HIGH RESOLUTION, FULLY REFINED VERSION OF 1DGC             
REMARK 900 THAT INCLUDES 46 WATER MOLECULES.                                    
REMARK 999                                                                      
REMARK 999 SEQUENCE                                                             
REMARK 999 AMINO ACID NUMBERING (RESIDUE NUMBER) CORRESPONDS TO THE             
REMARK 999 281 AMINO ACIDS OF INTACT GCN4.                                      
REMARK 999                                                                      
REMARK 999 RESIDUE NUMBERING OF NUCLEOTIDES:                                    
REMARK 999  5'  T  G  G  A  G  A  T  G  A  C  G  T  C  A  T  C  T               
REMARK 999    -10 -9 -8 -7 -6 -5 -4 -3 -2 -1  1  2  3  4  5  6  7               
REMARK 999                                                                      
REMARK 999   C  C  3'                                                           
REMARK 999   8  9                                                               
DBREF  2DGC A  220   281  UNP    P03069   GCN4_YEAST     220    281             
DBREF  2DGC B  -10     9  PDB    2DGC     2DGC           -10      9             
SEQRES   1 B   19   DT  DG  DG  DA  DG  DA  DT  DG  DA  DC  DG  DT  DC          
SEQRES   2 B   19   DA  DT  DC  DT  DC  DC                                      
SEQRES   1 A   63  MET ILE VAL PRO GLU SER SER ASP PRO ALA ALA LEU LYS          
SEQRES   2 A   63  ARG ALA ARG ASN THR GLU ALA ALA ARG ARG SER ARG ALA          
SEQRES   3 A   63  ARG LYS LEU GLN ARG MET LYS GLN LEU GLU ASP LYS VAL          
SEQRES   4 A   63  GLU GLU LEU LEU SER LYS ASN TYR HIS LEU GLU ASN GLU          
SEQRES   5 A   63  VAL ALA ARG LEU LYS LYS LEU VAL GLY GLU ARG                  
FORMUL   3  HOH   *46(H2 O)                                                     
HELIX    1   1 ALA A  229  LYS A  276  1                                  48    
CRYST1   58.660   58.660   86.880  90.00  90.00  90.00 P 41 21 2     8          
ORIGX1      1.000000  0.000000  0.000000        0.00000                         
ORIGX2      0.000000  1.000000  0.000000        0.00000                         
ORIGX3      0.000000  0.000000  1.000000        0.00000                         
SCALE1      0.017047  0.000000  0.000000        0.00000                         
SCALE2      0.000000  0.017047  0.000000        0.00000                         
SCALE3      0.000000  0.000000  0.011510        0.00000                         
ATOM      1  O5'  DT B -10      10.064  60.706  16.438  1.00 72.59           O  
ATOM      2  C5'  DT B -10       8.898  61.256  15.717  1.00 72.19           C  
ATOM      3  C4'  DT B -10       8.006  62.336  16.427  1.00 67.77           C  
ATOM      4  O4'  DT B -10       7.931  61.940  17.822  1.00 68.06           O  
ATOM      5  C3'  DT B -10       8.547  63.738  16.477  1.00 67.68           C  
ATOM      6  O3'  DT B -10       7.543  64.601  16.971  1.00 70.61           O  
ATOM      7  C2'  DT B -10       9.487  63.563  17.633  1.00 65.65           C  
ATOM      8  C1'  DT B -10       8.780  62.739  18.689  1.00 62.53           C  
ATOM      9  N1   DT B -10       9.758  62.016  19.586  1.00 56.32           N  
ATOM     10  C2   DT B -10       9.646  62.185  21.004  1.00 55.96           C  
ATOM     11  O2   DT B -10       8.790  62.857  21.587  1.00 53.10           O  
ATOM     12  N3   DT B -10      10.597  61.516  21.796  1.00 53.83           N  
ATOM     13  C4   DT B -10      11.633  60.705  21.293  1.00 53.07           C  
ATOM     14  O4   DT B -10      12.435  60.153  22.048  1.00 54.74           O  
ATOM     15  C5   DT B -10      11.659  60.588  19.846  1.00 50.67           C  
ATOM     16  C7   DT B -10      12.735  59.736  19.231  1.00 48.58           C  
ATOM     17  C6   DT B -10      10.766  61.222  19.059  1.00 51.74           C  
ATOM     18  P    DG B  -9       7.165  66.046  16.314  1.00 75.51           P  
ATOM     19  OP1  DG B  -9       5.882  65.838  15.568  1.00 76.59           O  
ATOM     20  OP2  DG B  -9       8.362  66.631  15.607  1.00 73.39           O  
ATOM     21  O5'  DG B  -9       6.762  66.991  17.601  1.00 72.42           O  
ATOM     22  C5'  DG B  -9       6.443  66.484  18.937  1.00 69.50           C  
ATOM     23  C4'  DG B  -9       7.523  66.823  20.025  1.00 66.10           C  
ATOM     24  O4'  DG B  -9       8.689  65.988  19.976  1.00 60.50           O  
ATOM     25  C3'  DG B  -9       7.993  68.265  19.739  1.00 65.79           C  
ATOM     26  O3'  DG B  -9       7.315  69.187  20.599  1.00 70.20           O  
ATOM     27  C2'  DG B  -9       9.498  68.227  19.697  1.00 58.81           C  
ATOM     28  C1'  DG B  -9       9.831  66.854  20.197  1.00 55.54           C  
ATOM     29  N9   DG B  -9      10.851  66.216  19.403  1.00 48.04           N  
ATOM     30  C8   DG B  -9      11.083  66.282  18.052  1.00 45.74           C  
ATOM     31  N7   DG B  -9      12.083  65.512  17.683  1.00 45.70           N  
ATOM     32  C5   DG B  -9      12.516  64.922  18.869  1.00 41.93           C  
ATOM     33  C6   DG B  -9      13.553  64.021  19.101  1.00 39.71           C  
ATOM     34  O6   DG B  -9      14.320  63.549  18.293  1.00 43.88           O  
ATOM     35  N1   DG B  -9      13.676  63.663  20.393  1.00 35.11           N  
ATOM     36  C2   DG B  -9      12.873  64.142  21.380  1.00 40.62           C  
ATOM     37  N2   DG B  -9      13.077  63.716  22.620  1.00 43.21           N  
ATOM     38  N3   DG B  -9      11.884  65.011  21.189  1.00 41.79           N  
ATOM     39  C4   DG B  -9      11.765  65.351  19.909  1.00 43.16           C  
ATOM     40  P    DG B  -8       8.077  70.120  21.666  1.00 75.00           P  
ATOM     41  OP1  DG B  -8       7.040  70.681  22.592  1.00 75.62           O  
ATOM     42  OP2  DG B  -8       8.974  71.059  20.907  1.00 74.14           O  
ATOM     43  O5'  DG B  -8       8.969  68.940  22.479  1.00 71.52           O  
ATOM     44  C5'  DG B  -8       9.226  68.777  23.891  1.00 65.23           C  
ATOM     45  C4'  DG B  -8      10.722  68.976  24.325  1.00 62.95           C  
ATOM     46  O4'  DG B  -8      11.698  68.185  23.579  1.00 60.14           O  
ATOM     47  C3'  DG B  -8      11.248  70.412  24.292  1.00 62.11           C  
ATOM     48  O3'  DG B  -8      12.291  70.444  25.263  1.00 66.29           O  
ATOM     49  C2'  DG B  -8      11.966  70.421  22.980  1.00 58.04           C  
ATOM     50  C1'  DG B  -8      12.698  69.101  23.056  1.00 53.52           C  
ATOM     51  N9   DG B  -8      13.253  68.685  21.770  1.00 45.40           N  
ATOM     52  C8   DG B  -8      12.943  69.103  20.513  1.00 42.65           C  
ATOM     53  N7   DG B  -8      13.660  68.507  19.599  1.00 40.98           N  
ATOM     54  C5   DG B  -8      14.492  67.652  20.299  1.00 35.95           C  
ATOM     55  C6   DG B  -8      15.465  66.762  19.834  1.00 33.35           C  
ATOM     56  O6   DG B  -8      15.792  66.529  18.683  1.00 31.75           O  
ATOM     57  N1   DG B  -8      16.072  66.109  20.849  1.00 31.69           N  
ATOM     58  C2   DG B  -8      15.778  66.269  22.169  1.00 34.20           C  
ATOM     59  N2   DG B  -8      16.440  65.541  23.045  1.00 36.41           N  
ATOM     60  N3   DG B  -8      14.873  67.101  22.636  1.00 37.25           N  
ATOM     61  C4   DG B  -8      14.254  67.758  21.631  1.00 40.31           C  
ATOM     62  P    DA B  -7      12.311  71.480  26.485  1.00 70.84           P  
ATOM     63  OP1  DA B  -7      11.139  71.111  27.360  1.00 69.10           O  
ATOM     64  OP2  DA B  -7      12.469  72.875  25.909  1.00 69.24           O  
ATOM     65  O5'  DA B  -7      13.717  71.098  27.234  1.00 63.53           O  
ATOM     66  C5'  DA B  -7      14.030  69.788  27.702  1.00 58.43           C  
ATOM     67  C4'  DA B  -7      15.520  69.459  27.492  1.00 55.18           C  
ATOM     68  O4'  DA B  -7      15.952  68.962  26.201  1.00 51.85           O  
ATOM     69  C3'  DA B  -7      16.353  70.668  27.797  1.00 53.14           C  
ATOM     70  O3'  DA B  -7      17.193  70.303  28.865  1.00 55.67           O  
ATOM     71  C2'  DA B  -7      17.095  70.875  26.520  1.00 49.15           C  
ATOM     72  C1'  DA B  -7      17.176  69.554  25.795  1.00 43.35           C  
ATOM     73  N9   DA B  -7      17.005  69.838  24.380  1.00 34.95           N  
ATOM     74  C8   DA B  -7      16.126  70.710  23.795  1.00 33.84           C  
ATOM     75  N7   DA B  -7      16.214  70.738  22.488  1.00 34.76           N  
ATOM     76  C5   DA B  -7      17.201  69.815  22.203  1.00 27.79           C  
ATOM     77  C6   DA B  -7      17.740  69.378  21.004  1.00 28.28           C  
ATOM     78  N6   DA B  -7      17.351  69.843  19.819  1.00 27.91           N  
ATOM     79  N1   DA B  -7      18.701  68.454  21.071  1.00 28.05           N  
ATOM     80  C2   DA B  -7      19.083  67.987  22.252  1.00 27.78           C  
ATOM     81  N3   DA B  -7      18.642  68.325  23.450  1.00 31.14           N  
ATOM     82  C4   DA B  -7      17.681  69.261  23.349  1.00 30.91           C  
ATOM     83  P    DG B  -6      18.239  71.295  29.548  1.00 55.92           P  
ATOM     84  OP1  DG B  -6      18.379  70.795  30.944  1.00 57.50           O  
ATOM     85  OP2  DG B  -6      17.780  72.662  29.273  1.00 57.05           O  
ATOM     86  O5'  DG B  -6      19.579  71.023  28.710  1.00 50.50           O  
ATOM     87  C5'  DG B  -6      20.269  69.785  28.895  1.00 43.67           C  
ATOM     88  C4'  DG B  -6      21.390  69.525  27.876  1.00 37.92           C  
ATOM     89  O4'  DG B  -6      20.918  69.692  26.544  1.00 36.54           O  
ATOM     90  C3'  DG B  -6      22.589  70.437  28.025  1.00 36.69           C  
ATOM     91  O3'  DG B  -6      23.769  69.619  27.951  1.00 37.67           O  
ATOM     92  C2'  DG B  -6      22.401  71.376  26.860  1.00 36.04           C  
ATOM     93  C1'  DG B  -6      21.832  70.490  25.796  1.00 32.72           C  
ATOM     94  N9   DG B  -6      21.079  71.184  24.777  1.00 28.09           N  
ATOM     95  C8   DG B  -6      20.061  72.122  24.889  1.00 25.03           C  
ATOM     96  N7   DG B  -6      19.561  72.497  23.718  1.00 28.31           N  
ATOM     97  C5   DG B  -6      20.325  71.751  22.791  1.00 29.36           C  
ATOM     98  C6   DG B  -6      20.274  71.727  21.346  1.00 31.49           C  
ATOM     99  O6   DG B  -6      19.528  72.376  20.594  1.00 30.35           O  
ATOM    100  N1   DG B  -6      21.211  70.812  20.808  1.00 28.07           N  
ATOM    101  C2   DG B  -6      22.067  70.051  21.563  1.00 27.04           C  
ATOM    102  N2   DG B  -6      22.860  69.268  20.867  1.00 24.45           N  
ATOM    103  N3   DG B  -6      22.134  70.094  22.916  1.00 26.34           N  
ATOM    104  C4   DG B  -6      21.238  70.948  23.449  1.00 26.76           C  
ATOM    105  P    DA B  -5      25.194  70.302  28.050  1.00 37.88           P  
ATOM    106  OP1  DA B  -5      26.136  69.457  28.782  1.00 40.74           O  
ATOM    107  OP2  DA B  -5      25.001  71.712  28.444  1.00 36.58           O  
ATOM    108  O5'  DA B  -5      25.590  70.159  26.541  1.00 39.43           O  
ATOM    109  C5'  DA B  -5      26.142  68.957  26.005  1.00 34.15           C  
ATOM    110  C4'  DA B  -5      26.825  69.266  24.662  1.00 30.41           C  
ATOM    111  O4'  DA B  -5      25.931  69.898  23.731  1.00 27.09           O  
ATOM    112  C3'  DA B  -5      27.928  70.219  24.830  1.00 29.13           C  
ATOM    113  O3'  DA B  -5      29.036  69.606  24.218  1.00 33.87           O  
ATOM    114  C2'  DA B  -5      27.421  71.473  24.125  1.00 26.25           C  
ATOM    115  C1'  DA B  -5      26.406  71.080  23.132  1.00 22.99           C  
ATOM    116  N9   DA B  -5      25.264  72.001  23.099  1.00 20.86           N  
ATOM    117  C8   DA B  -5      24.551  72.503  24.131  1.00 20.80           C  
ATOM    118  N7   DA B  -5      23.569  73.265  23.767  1.00 22.53           N  
ATOM    119  C5   DA B  -5      23.623  73.279  22.381  1.00 17.47           C  
ATOM    120  C6   DA B  -5      22.851  73.915  21.398  1.00 18.29           C  
ATOM    121  N6   DA B  -5      21.814  74.723  21.632  1.00 18.45           N  
ATOM    122  N1   DA B  -5      23.174  73.708  20.127  1.00 19.12           N  
ATOM    123  C2   DA B  -5      24.211  72.906  19.863  1.00 22.47           C  
ATOM    124  N3   DA B  -5      25.027  72.274  20.691  1.00 23.17           N  
ATOM    125  C4   DA B  -5      24.657  72.501  21.971  1.00 21.35           C  
ATOM    126  P    DT B  -4      30.443  70.323  24.193  1.00 37.08           P  
ATOM    127  OP1  DT B  -4      31.486  69.287  24.147  1.00 39.23           O  
ATOM    128  OP2  DT B  -4      30.561  71.395  25.218  1.00 39.08           O  
ATOM    129  O5'  DT B  -4      30.357  71.104  22.790  1.00 37.55           O  
ATOM    130  C5'  DT B  -4      30.272  70.496  21.505  1.00 34.07           C  
ATOM    131  C4'  DT B  -4      30.017  71.592  20.496  1.00 32.60           C  
ATOM    132  O4'  DT B  -4      28.751  72.257  20.707  1.00 29.62           O  
ATOM    133  C3'  DT B  -4      31.119  72.606  20.590  1.00 35.19           C  
ATOM    134  O3'  DT B  -4      31.822  72.452  19.331  1.00 44.23           O  
ATOM    135  C2'  DT B  -4      30.304  73.871  20.776  1.00 31.17           C  
ATOM    136  C1'  DT B  -4      28.916  73.567  20.275  1.00 26.00           C  
ATOM    137  N1   DT B  -4      27.878  74.430  20.828  1.00 25.36           N  
ATOM    138  C2   DT B  -4      27.045  75.077  19.943  1.00 26.33           C  
ATOM    139  O2   DT B  -4      27.104  74.969  18.720  1.00 27.90           O  
ATOM    140  N3   DT B  -4      26.096  75.905  20.510  1.00 26.03           N  
ATOM    141  C4   DT B  -4      25.886  76.149  21.843  1.00 22.82           C  
ATOM    142  O4   DT B  -4      24.985  76.912  22.155  1.00 29.07           O  
ATOM    143  C5   DT B  -4      26.774  75.456  22.717  1.00 22.68           C  
ATOM    144  C7   DT B  -4      26.661  75.621  24.233  1.00 21.35           C  
ATOM    145  C6   DT B  -4      27.726  74.629  22.192  1.00 25.56           C  
ATOM    146  P    DG B  -3      33.371  72.815  18.869  1.00 49.86           P  
ATOM    147  OP1  DG B  -3      34.018  71.576  18.326  1.00 51.18           O  
ATOM    148  OP2  DG B  -3      34.125  73.600  19.881  1.00 51.54           O  
ATOM    149  O5'  DG B  -3      32.938  73.898  17.749  1.00 47.23           O  
ATOM    150  C5'  DG B  -3      32.394  73.533  16.492  1.00 42.95           C  
ATOM    151  C4'  DG B  -3      32.020  74.740  15.678  1.00 39.94           C  
ATOM    152  O4'  DG B  -3      30.772  75.304  16.105  1.00 37.07           O  
ATOM    153  C3'  DG B  -3      33.119  75.805  15.644  1.00 39.96           C  
ATOM    154  O3'  DG B  -3      33.198  76.316  14.288  1.00 47.94           O  
ATOM    155  C2'  DG B  -3      32.460  76.837  16.526  1.00 37.78           C  
ATOM    156  C1'  DG B  -3      30.949  76.724  16.279  1.00 32.41           C  
ATOM    157  N9   DG B  -3      30.258  77.110  17.536  1.00 28.39           N  
ATOM    158  C8   DG B  -3      30.624  76.740  18.821  1.00 20.81           C  
ATOM    159  N7   DG B  -3      29.855  77.231  19.734  1.00 22.44           N  
ATOM    160  C5   DG B  -3      28.892  77.957  19.014  1.00 22.55           C  
ATOM    161  C6   DG B  -3      27.779  78.702  19.470  1.00 20.66           C  
ATOM    162  O6   DG B  -3      27.422  78.864  20.618  1.00 23.05           O  
ATOM    163  N1   DG B  -3      27.066  79.295  18.454  1.00 18.98           N  
ATOM    164  C2   DG B  -3      27.374  79.191  17.123  1.00 16.47           C  
ATOM    165  N2   DG B  -3      26.586  79.826  16.259  1.00 18.60           N  
ATOM    166  N3   DG B  -3      28.412  78.511  16.685  1.00 15.52           N  
ATOM    167  C4   DG B  -3      29.124  77.895  17.664  1.00 21.47           C  
ATOM    168  P    DA B  -2      34.309  77.326  13.582  1.00 49.40           P  
ATOM    169  OP1  DA B  -2      34.280  76.983  12.133  1.00 51.49           O  
ATOM    170  OP2  DA B  -2      35.563  77.225  14.386  1.00 46.83           O  
ATOM    171  O5'  DA B  -2      33.735  78.836  13.694  1.00 43.65           O  
ATOM    172  C5'  DA B  -2      32.758  79.183  12.726  1.00 39.97           C  
ATOM    173  C4'  DA B  -2      32.045  80.486  13.006  1.00 38.42           C  
ATOM    174  O4'  DA B  -2      31.211  80.370  14.177  1.00 36.33           O  
ATOM    175  C3'  DA B  -2      33.003  81.653  13.157  1.00 38.65           C  
ATOM    176  O3'  DA B  -2      32.685  82.677  12.169  1.00 39.94           O  
ATOM    177  C2'  DA B  -2      32.707  82.030  14.614  1.00 35.76           C  
ATOM    178  C1'  DA B  -2      31.272  81.580  14.892  1.00 33.88           C  
ATOM    179  N9   DA B  -2      31.070  81.293  16.320  1.00 30.09           N  
ATOM    180  C8   DA B  -2      31.891  80.546  17.099  1.00 28.10           C  
ATOM    181  N7   DA B  -2      31.474  80.442  18.325  1.00 28.61           N  
ATOM    182  C5   DA B  -2      30.291  81.186  18.392  1.00 25.44           C  
ATOM    183  C6   DA B  -2      29.386  81.459  19.452  1.00 23.76           C  
ATOM    184  N6   DA B  -2      29.585  80.975  20.671  1.00 17.26           N  
ATOM    185  N1   DA B  -2      28.301  82.199  19.201  1.00 23.27           N  
ATOM    186  C2   DA B  -2      28.138  82.648  17.962  1.00 25.20           C  
ATOM    187  N3   DA B  -2      28.908  82.479  16.877  1.00 24.13           N  
ATOM    188  C4   DA B  -2      30.005  81.709  17.160  1.00 27.52           C  
ATOM    189  P    DC B  -1      33.328  84.190  12.033  1.00 40.87           P  
ATOM    190  OP1  DC B  -1      33.253  84.509  10.582  1.00 43.73           O  
ATOM    191  OP2  DC B  -1      34.634  84.269  12.734  1.00 42.20           O  
ATOM    192  O5'  DC B  -1      32.366  85.117  12.795  1.00 35.14           O  
ATOM    193  C5'  DC B  -1      30.994  85.097  12.509  1.00 32.57           C  
ATOM    194  C4'  DC B  -1      30.261  85.793  13.632  1.00 30.36           C  
ATOM    195  O4'  DC B  -1      30.262  85.034  14.839  1.00 26.71           O  
ATOM    196  C3'  DC B  -1      30.955  87.116  13.945  1.00 27.62           C  
ATOM    197  O3'  DC B  -1      30.438  88.095  13.019  1.00 26.47           O  
ATOM    198  C2'  DC B  -1      30.492  87.332  15.363  1.00 26.65           C  
ATOM    199  C1'  DC B  -1      30.096  86.006  15.865  1.00 23.74           C  
ATOM    200  N1   DC B  -1      30.799  85.420  16.991  1.00 22.77           N  
ATOM    201  C2   DC B  -1      30.182  85.559  18.240  1.00 22.63           C  
ATOM    202  O2   DC B  -1      29.145  86.217  18.381  1.00 22.04           O  
ATOM    203  N3   DC B  -1      30.782  84.936  19.321  1.00 23.17           N  
ATOM    204  C4   DC B  -1      31.927  84.206  19.176  1.00 19.24           C  
ATOM    205  N4   DC B  -1      32.441  83.640  20.258  1.00 15.84           N  
ATOM    206  C5   DC B  -1      32.566  84.047  17.878  1.00 19.62           C  
ATOM    207  C6   DC B  -1      31.964  84.669  16.831  1.00 20.89           C  
ATOM    208  P    DG B   1      31.093  89.483  12.867  1.00 28.75           P  
ATOM    209  OP1  DG B   1      30.494  90.192  11.700  1.00 32.35           O  
ATOM    210  OP2  DG B   1      32.549  89.207  12.940  1.00 27.19           O  
ATOM    211  O5'  DG B   1      30.698  90.417  14.082  1.00 31.16           O  
ATOM    212  C5'  DG B   1      29.426  90.976  14.391  1.00 29.21           C  
ATOM    213  C4'  DG B   1      29.491  91.499  15.844  1.00 30.37           C  
ATOM    214  O4'  DG B   1      29.855  90.364  16.732  1.00 30.64           O  
ATOM    215  C3'  DG B   1      30.519  92.677  16.067  1.00 31.19           C  
ATOM    216  O3'  DG B   1      29.803  93.813  16.671  1.00 31.90           O  
ATOM    217  C2'  DG B   1      31.577  91.984  16.955  1.00 27.05           C  
ATOM    218  C1'  DG B   1      30.807  90.872  17.651  1.00 24.90           C  
ATOM    219  N9   DG B   1      31.626  89.791  18.097  1.00 21.55           N  
ATOM    220  C8   DG B   1      32.591  89.132  17.445  1.00 19.42           C  
ATOM    221  N7   DG B   1      33.168  88.212  18.156  1.00 20.16           N  
ATOM    222  C5   DG B   1      32.548  88.273  19.386  1.00 19.17           C  
ATOM    223  C6   DG B   1      32.771  87.517  20.532  1.00 18.55           C  
ATOM    224  O6   DG B   1      33.561  86.602  20.703  1.00 22.22           O  
ATOM    225  N1   DG B   1      31.962  87.895  21.531  1.00 18.19           N  
ATOM    226  C2   DG B   1      31.026  88.881  21.436  1.00 19.17           C  
ATOM    227  N2   DG B   1      30.319  89.125  22.519  1.00 21.72           N  
ATOM    228  N3   DG B   1      30.783  89.609  20.362  1.00 19.54           N  
ATOM    229  C4   DG B   1      31.596  89.248  19.366  1.00 22.13           C  
ATOM    230  P    DT B   2      30.224  95.327  17.064  1.00 38.07           P  
ATOM    231  OP1  DT B   2      28.952  96.084  17.066  1.00 38.06           O  
ATOM    232  OP2  DT B   2      31.335  95.813  16.217  1.00 35.11           O  
ATOM    233  O5'  DT B   2      30.725  95.317  18.596  1.00 36.75           O  
ATOM    234  C5'  DT B   2      29.730  95.076  19.607  1.00 35.17           C  
ATOM    235  C4'  DT B   2      30.230  94.620  20.957  1.00 34.38           C  
ATOM    236  O4'  DT B   2      30.866  93.349  20.917  1.00 34.01           O  
ATOM    237  C3'  DT B   2      31.252  95.606  21.348  1.00 36.90           C  
ATOM    238  O3'  DT B   2      30.653  96.542  22.211  1.00 44.64           O  
ATOM    239  C2'  DT B   2      32.370  94.803  21.976  1.00 36.67           C  
ATOM    240  C1'  DT B   2      31.935  93.366  21.906  1.00 32.98           C  
ATOM    241  N1   DT B   2      32.992  92.405  21.515  1.00 29.28           N  
ATOM    242  C2   DT B   2      33.396  91.478  22.446  1.00 27.33           C  
ATOM    243  O2   DT B   2      32.976  91.425  23.575  1.00 29.71           O  
ATOM    244  N3   DT B   2      34.336  90.559  22.076  1.00 27.10           N  
ATOM    245  C4   DT B   2      34.942  90.478  20.834  1.00 26.04           C  
ATOM    246  O4   DT B   2      35.784  89.592  20.639  1.00 28.37           O  
ATOM    247  C5   DT B   2      34.487  91.496  19.879  1.00 27.05           C  
ATOM    248  C7   DT B   2      35.088  91.531  18.440  1.00 20.03           C  
ATOM    249  C6   DT B   2      33.532  92.402  20.249  1.00 27.37           C  
ATOM    250  P    DC B   3      31.437  97.899  22.683  1.00 50.37           P  
ATOM    251  OP1  DC B   3      30.435  98.988  22.834  1.00 52.71           O  
ATOM    252  OP2  DC B   3      32.653  98.167  21.860  1.00 52.26           O  
ATOM    253  O5'  DC B   3      32.028  97.425  24.128  1.00 49.39           O  
ATOM    254  C5'  DC B   3      31.350  96.808  25.228  1.00 41.05           C  
ATOM    255  C4'  DC B   3      32.364  96.246  26.196  1.00 36.75           C  
ATOM    256  O4'  DC B   3      32.995  95.143  25.620  1.00 32.97           O  
ATOM    257  C3'  DC B   3      33.494  97.202  26.532  1.00 40.79           C  
ATOM    258  O3'  DC B   3      33.628  97.235  27.955  1.00 50.66           O  
ATOM    259  C2'  DC B   3      34.725  96.548  25.938  1.00 36.17           C  
ATOM    260  C1'  DC B   3      34.391  95.082  25.963  1.00 33.01           C  
ATOM    261  N1   DC B   3      35.184  94.358  24.929  1.00 31.42           N  
ATOM    262  C2   DC B   3      35.859  93.154  25.237  1.00 34.11           C  
ATOM    263  O2   DC B   3      35.878  92.632  26.358  1.00 36.41           O  
ATOM    264  N3   DC B   3      36.567  92.529  24.223  1.00 31.93           N  
ATOM    265  C4   DC B   3      36.635  93.046  23.000  1.00 23.62           C  
ATOM    266  N4   DC B   3      37.346  92.421  22.090  1.00 22.49           N  
ATOM    267  C5   DC B   3      35.950  94.238  22.671  1.00 25.13           C  
ATOM    268  C6   DC B   3      35.256  94.862  23.652  1.00 29.29           C  
ATOM    269  P    DA B   4      34.526  98.317  28.803  1.00 53.15           P  
ATOM    270  OP1  DA B   4      33.602  98.855  29.828  1.00 53.27           O  
ATOM    271  OP2  DA B   4      35.208  99.242  27.858  1.00 53.08           O  
ATOM    272  O5'  DA B   4      35.678  97.477  29.513  1.00 48.98           O  
ATOM    273  C5'  DA B   4      35.392  96.316  30.263  1.00 47.78           C  
ATOM    274  C4'  DA B   4      36.675  95.529  30.406  1.00 48.68           C  
ATOM    275  O4'  DA B   4      37.048  94.916  29.185  1.00 48.62           O  
ATOM    276  C3'  DA B   4      37.846  96.453  30.768  1.00 50.36           C  
ATOM    277  O3'  DA B   4      38.116  96.132  32.133  1.00 53.85           O  
ATOM    278  C2'  DA B   4      38.939  96.159  29.758  1.00 46.97           C  
ATOM    279  C1'  DA B   4      38.487  94.920  29.014  1.00 42.77           C  
ATOM    280  N9   DA B   4      38.664  95.042  27.557  1.00 32.37           N  
ATOM    281  C8   DA B   4      38.116  95.989  26.742  1.00 33.65           C  
ATOM    282  N7   DA B   4      38.419  95.836  25.478  1.00 32.95           N  
ATOM    283  C5   DA B   4      39.213  94.692  25.478  1.00 28.45           C  
ATOM    284  C6   DA B   4      39.867  94.011  24.449  1.00 27.01           C  
ATOM    285  N6   DA B   4      39.790  94.396  23.180  1.00 28.28           N  
ATOM    286  N1   DA B   4      40.574  92.931  24.788  1.00 25.73           N  
ATOM    287  C2   DA B   4      40.626  92.589  26.068  1.00 26.37           C  
ATOM    288  N3   DA B   4      40.057  93.160  27.112  1.00 23.99           N  
ATOM    289  C4   DA B   4      39.350  94.207  26.744  1.00 26.88           C  
ATOM    290  P    DT B   5      39.412  96.375  33.014  1.00 54.54           P  
ATOM    291  OP1  DT B   5      38.899  96.290  34.399  1.00 58.30           O  
ATOM    292  OP2  DT B   5      40.185  97.575  32.575  1.00 52.85           O  
ATOM    293  O5'  DT B   5      40.263  95.050  32.710  1.00 53.16           O  
ATOM    294  C5'  DT B   5      41.663  95.237  32.595  1.00 50.26           C  
ATOM    295  C4'  DT B   5      42.280  94.489  31.449  1.00 48.93           C  
ATOM    296  O4'  DT B   5      41.785  94.794  30.147  1.00 42.74           O  
ATOM    297  C3'  DT B   5      43.663  94.996  31.464  1.00 49.30           C  
ATOM    298  O3'  DT B   5      44.355  94.098  32.289  1.00 55.87           O  
ATOM    299  C2'  DT B   5      44.131  94.945  30.056  1.00 45.33           C  
ATOM    300  C1'  DT B   5      42.921  94.556  29.305  1.00 40.50           C  
ATOM    301  N1   DT B   5      42.744  95.248  28.014  1.00 35.46           N  
ATOM    302  C2   DT B   5      43.192  94.584  26.850  1.00 34.47           C  
ATOM    303  O2   DT B   5      43.759  93.472  26.884  1.00 33.42           O  
ATOM    304  N3   DT B   5      42.957  95.270  25.652  1.00 31.80           N  
ATOM    305  C4   DT B   5      42.326  96.499  25.551  1.00 32.21           C  
ATOM    306  O4   DT B   5      42.152  97.019  24.458  1.00 33.26           O  
ATOM    307  C5   DT B   5      41.912  97.072  26.814  1.00 32.51           C  
ATOM    308  C7   DT B   5      41.200  98.399  26.831  1.00 33.08           C  
ATOM    309  C6   DT B   5      42.126  96.456  27.970  1.00 29.72           C  
ATOM    310  P    DC B   6      45.851  94.498  32.703  1.00 63.20           P  
ATOM    311  OP1  DC B   6      46.170  93.753  33.974  1.00 60.92           O  
ATOM    312  OP2  DC B   6      45.927  96.004  32.679  1.00 60.54           O  
ATOM    313  O5'  DC B   6      46.755  93.930  31.400  1.00 61.51           O  
ATOM    314  C5'  DC B   6      47.071  92.545  31.143  1.00 62.41           C  
ATOM    315  C4'  DC B   6      47.887  92.262  29.860  1.00 63.49           C  
ATOM    316  O4'  DC B   6      47.240  92.727  28.635  1.00 61.56           O  
ATOM    317  C3'  DC B   6      49.232  92.924  29.958  1.00 66.91           C  
ATOM    318  O3'  DC B   6      50.353  92.000  29.703  1.00 76.49           O  
ATOM    319  C2'  DC B   6      49.066  94.068  28.952  1.00 63.03           C  
ATOM    320  C1'  DC B   6      48.094  93.596  27.866  1.00 56.94           C  
ATOM    321  N1   DC B   6      47.339  94.761  27.266  1.00 50.41           N  
ATOM    322  C2   DC B   6      47.125  94.837  25.873  1.00 46.88           C  
ATOM    323  O2   DC B   6      47.544  93.996  25.085  1.00 46.11           O  
ATOM    324  N3   DC B   6      46.440  95.905  25.362  1.00 43.11           N  
ATOM    325  C4   DC B   6      45.982  96.871  26.167  1.00 41.29           C  
ATOM    326  N4   DC B   6      45.327  97.887  25.640  1.00 38.57           N  
ATOM    327  C5   DC B   6      46.183  96.821  27.584  1.00 43.24           C  
ATOM    328  C6   DC B   6      46.863  95.762  28.081  1.00 46.68           C  
ATOM    329  P    DT B   7      51.972  92.557  29.501  1.00 83.48           P  
ATOM    330  OP1  DT B   7      52.956  91.440  29.716  1.00 81.80           O  
ATOM    331  OP2  DT B   7      52.163  93.914  30.152  1.00 81.39           O  
ATOM    332  O5'  DT B   7      51.918  92.800  27.943  1.00 80.19           O  
ATOM    333  C5'  DT B   7      51.564  91.744  27.026  1.00 76.72           C  
ATOM    334  C4'  DT B   7      51.842  92.283  25.672  1.00 72.71           C  
ATOM    335  O4'  DT B   7      51.050  93.464  25.446  1.00 68.29           O  
ATOM    336  C3'  DT B   7      53.278  92.768  25.786  1.00 74.09           C  
ATOM    337  O3'  DT B   7      53.915  92.065  24.729  1.00 80.55           O  
ATOM    338  C2'  DT B   7      53.170  94.326  25.806  1.00 67.92           C  
ATOM    339  C1'  DT B   7      51.887  94.568  25.043  1.00 60.72           C  
ATOM    340  N1   DT B   7      51.078  95.773  25.275  1.00 50.97           N  
ATOM    341  C2   DT B   7      50.520  96.399  24.174  1.00 47.37           C  
ATOM    342  O2   DT B   7      50.682  96.067  23.012  1.00 47.82           O  
ATOM    343  N3   DT B   7      49.735  97.480  24.400  1.00 44.00           N  
ATOM    344  C4   DT B   7      49.430  98.027  25.596  1.00 44.90           C  
ATOM    345  O4   DT B   7      48.705  99.012  25.643  1.00 44.57           O  
ATOM    346  C5   DT B   7      50.026  97.334  26.707  1.00 47.27           C  
ATOM    347  C7   DT B   7      49.764  97.849  28.115  1.00 47.02           C  
ATOM    348  C6   DT B   7      50.809  96.235  26.520  1.00 49.30           C  
ATOM    349  P    DC B   8      55.534  92.114  24.522  1.00 87.23           P  
ATOM    350  OP1  DC B   8      56.059  90.713  24.722  1.00 84.79           O  
ATOM    351  OP2  DC B   8      56.121  93.276  25.288  1.00 84.97           O  
ATOM    352  O5'  DC B   8      55.468  92.509  22.896  1.00 84.40           O  
ATOM    353  C5'  DC B   8      54.595  93.597  22.498  1.00 79.72           C  
ATOM    354  C4'  DC B   8      55.258  94.733  21.715  1.00 76.89           C  
ATOM    355  O4'  DC B   8      54.370  95.887  21.793  1.00 72.95           O  
ATOM    356  C3'  DC B   8      56.657  95.183  22.195  1.00 76.38           C  
ATOM    357  O3'  DC B   8      57.426  95.569  21.015  1.00 78.97           O  
ATOM    358  C2'  DC B   8      56.256  96.380  23.014  1.00 72.53           C  
ATOM    359  C1'  DC B   8      55.058  97.020  22.299  1.00 67.02           C  
ATOM    360  N1   DC B   8      54.248  97.799  23.257  1.00 61.49           N  
ATOM    361  C2   DC B   8      53.426  98.853  22.832  1.00 58.43           C  
ATOM    362  O2   DC B   8      53.308  99.190  21.663  1.00 54.68           O  
ATOM    363  N3   DC B   8      52.721  99.559  23.770  1.00 56.59           N  
ATOM    364  C4   DC B   8      52.807  99.247  25.082  1.00 57.43           C  
ATOM    365  N4   DC B   8      52.121  99.920  26.004  1.00 55.22           N  
ATOM    366  C5   DC B   8      53.639  98.171  25.530  1.00 59.02           C  
ATOM    367  C6   DC B   8      54.320  97.484  24.587  1.00 60.69           C  
ATOM    368  P    DC B   9      58.858  96.421  20.898  1.00 80.32           P  
ATOM    369  OP1  DC B   9      59.996  95.473  21.146  1.00 79.72           O  
ATOM    370  OP2  DC B   9      58.770  97.671  21.716  1.00 76.16           O  
ATOM    371  O5'  DC B   9      58.810  96.773  19.254  1.00 77.46           O  
ATOM    372  C5'  DC B   9      59.352  97.982  18.686  1.00 74.74           C  
ATOM    373  C4'  DC B   9      58.315  99.099  18.463  1.00 73.26           C  
ATOM    374  O4'  DC B   9      57.240  99.043  19.416  1.00 72.11           O  
ATOM    375  C3'  DC B   9      58.982 100.475  18.690  1.00 73.77           C  
ATOM    376  O3'  DC B   9      59.648 100.985  17.525  1.00 75.33           O  
ATOM    377  C2'  DC B   9      57.840 101.354  19.131  1.00 72.62           C  
ATOM    378  C1'  DC B   9      56.777 100.389  19.662  1.00 71.37           C  
ATOM    379  N1   DC B   9      56.488 100.617  21.114  1.00 70.64           N  
ATOM    380  C2   DC B   9      55.539 101.592  21.468  1.00 67.74           C  
ATOM    381  O2   DC B   9      54.956 102.255  20.623  1.00 64.30           O  
ATOM    382  N3   DC B   9      55.261 101.806  22.781  1.00 64.61           N  
ATOM    383  C4   DC B   9      55.907 101.086  23.717  1.00 67.72           C  
ATOM    384  N4   DC B   9      55.631 101.303  24.997  1.00 69.09           N  
ATOM    385  C5   DC B   9      56.883 100.077  23.393  1.00 67.79           C  
ATOM    386  C6   DC B   9      57.137  99.884  22.084  1.00 69.53           C  
TER     387       DC B   9                                                      
ATOM    388  N   ALA A 229      31.102 102.332  14.706  1.00 61.77           N  
ATOM    389  CA  ALA A 229      32.361 103.092  14.947  1.00 61.06           C  
ATOM    390  C   ALA A 229      33.518 102.392  14.237  1.00 59.88           C  
ATOM    391  O   ALA A 229      33.406 101.224  13.867  1.00 59.19           O  
ATOM    392  CB  ALA A 229      32.642 103.207  16.451  1.00 58.74           C  
ATOM    393  N   LEU A 230      34.628 103.112  14.085  1.00 58.68           N  
ATOM    394  CA  LEU A 230      35.824 102.612  13.415  1.00 56.53           C  
ATOM    395  C   LEU A 230      36.711 101.675  14.232  1.00 53.67           C  
ATOM    396  O   LEU A 230      37.188 100.665  13.706  1.00 55.13           O  
ATOM    397  CB  LEU A 230      36.642 103.789  12.880  1.00 59.17           C  
ATOM    398  CG  LEU A 230      36.280 104.302  11.480  1.00 60.56           C  
ATOM    399  CD1 LEU A 230      34.776 104.318  11.257  1.00 56.68           C  
ATOM    400  CD2 LEU A 230      36.889 105.686  11.281  1.00 63.15           C  
ATOM    401  N   LYS A 231      36.968 102.014  15.494  1.00 50.96           N  
ATOM    402  CA  LYS A 231      37.791 101.154  16.349  1.00 45.92           C  
ATOM    403  C   LYS A 231      37.091  99.810  16.534  1.00 38.45           C  
ATOM    404  O   LYS A 231      37.735  98.783  16.650  1.00 37.77           O  
ATOM    405  CB  LYS A 231      38.050 101.801  17.715  1.00 47.59           C  
ATOM    406  CG  LYS A 231      36.790 102.155  18.488  0.50 49.61           C  
ATOM    407  CD  LYS A 231      37.060 102.282  19.979  0.50 48.66           C  
ATOM    408  CE  LYS A 231      35.791 102.657  20.734  0.50 48.60           C  
ATOM    409  NZ  LYS A 231      34.658 101.721  20.470  0.50 43.12           N  
ATOM    410  N   ARG A 232      35.766  99.822  16.548  1.00 35.56           N  
ATOM    411  CA  ARG A 232      35.017  98.588  16.693  1.00 39.96           C  
ATOM    412  C   ARG A 232      35.206  97.711  15.450  1.00 41.71           C  
ATOM    413  O   ARG A 232      35.486  96.511  15.558  1.00 43.88           O  
ATOM    414  CB  ARG A 232      33.535  98.884  16.932  1.00 42.42           C  
ATOM    415  CG  ARG A 232      33.272  99.676  18.205  1.00 47.65           C  
ATOM    416  CD  ARG A 232      31.834  99.560  18.668  1.00 53.76           C  
ATOM    417  NE  ARG A 232      30.891  99.911  17.611  1.00 65.47           N  
ATOM    418  CZ  ARG A 232      29.714  99.313  17.431  1.00 72.34           C  
ATOM    419  NH1 ARG A 232      29.334  98.331  18.244  1.00 73.64           N  
ATOM    420  NH2 ARG A 232      28.918  99.688  16.431  1.00 72.78           N  
ATOM    421  N   ALA A 233      35.107  98.329  14.274  1.00 40.97           N  
ATOM    422  CA  ALA A 233      35.265  97.630  13.005  1.00 34.50           C  
ATOM    423  C   ALA A 233      36.605  96.929  12.935  1.00 31.37           C  
ATOM    424  O   ALA A 233      36.679  95.768  12.536  1.00 32.87           O  
ATOM    425  CB  ALA A 233      35.124  98.599  11.850  1.00 36.69           C  
ATOM    426  N   ARG A 234      37.662  97.636  13.318  1.00 28.78           N  
ATOM    427  CA  ARG A 234      39.005  97.063  13.309  1.00 32.08           C  
ATOM    428  C   ARG A 234      39.137  95.906  14.301  1.00 32.05           C  
ATOM    429  O   ARG A 234      39.730  94.867  13.974  1.00 34.03           O  
ATOM    430  CB  ARG A 234      40.064  98.126  13.625  1.00 33.37           C  
ATOM    431  CG  ARG A 234      40.145  99.252  12.610  1.00 45.36           C  
ATOM    432  CD  ARG A 234      41.480  99.993  12.675  1.00 48.37           C  
ATOM    433  NE  ARG A 234      42.624  99.115  12.420  1.00 50.34           N  
ATOM    434  CZ  ARG A 234      43.013  98.709  11.216  1.00 54.49           C  
ATOM    435  NH1 ARG A 234      42.355  99.094  10.133  1.00 57.96           N  
ATOM    436  NH2 ARG A 234      44.066  97.908  11.095  1.00 56.58           N  
ATOM    437  N   ASN A 235      38.562  96.072  15.496  1.00 30.84           N  
ATOM    438  CA  ASN A 235      38.630  95.043  16.532  1.00 29.17           C  
ATOM    439  C   ASN A 235      37.872  93.802  16.113  1.00 24.29           C  
ATOM    440  O   ASN A 235      38.297  92.687  16.404  1.00 29.82           O  
ATOM    441  CB  ASN A 235      38.121  95.559  17.885  1.00 28.69           C  
ATOM    442  CG  ASN A 235      38.282  94.531  19.003  1.00 26.68           C  
ATOM    443  OD1 ASN A 235      37.295  94.037  19.559  1.00 28.43           O  
ATOM    444  ND2 ASN A 235      39.523  94.198  19.329  1.00 22.08           N  
ATOM    445  N   THR A 236      36.775  93.982  15.389  1.00 24.56           N  
ATOM    446  CA  THR A 236      35.989  92.846  14.908  1.00 25.51           C  
ATOM    447  C   THR A 236      36.812  91.956  13.956  1.00 25.72           C  
ATOM    448  O   THR A 236      36.664  90.729  13.945  1.00 24.25           O  
ATOM    449  CB  THR A 236      34.696  93.326  14.251  1.00 21.98           C  
ATOM    450  OG1 THR A 236      33.946  94.054  15.219  1.00 29.98           O  
ATOM    451  CG2 THR A 236      33.848  92.166  13.771  1.00 27.12           C  
ATOM    452  N   GLU A 237      37.724  92.577  13.211  1.00 27.78           N  
ATOM    453  CA  GLU A 237      38.577  91.836  12.291  1.00 25.16           C  
ATOM    454  C   GLU A 237      39.767  91.272  13.028  1.00 20.89           C  
ATOM    455  O   GLU A 237      40.217  90.171  12.723  1.00 23.91           O  
ATOM    456  CB  GLU A 237      39.038  92.714  11.122  1.00 27.59           C  
ATOM    457  CG  GLU A 237      37.952  92.991  10.101  1.00 24.60           C  
ATOM    458  CD  GLU A 237      37.186  91.741   9.718  1.00 25.05           C  
ATOM    459  OE1 GLU A 237      37.803  90.773   9.240  1.00 29.46           O  
ATOM    460  OE2 GLU A 237      35.962  91.712   9.924  1.00 29.88           O  
ATOM    461  N   ALA A 238      40.277  92.018  14.003  1.00 21.91           N  
ATOM    462  CA  ALA A 238      41.416  91.539  14.786  1.00 24.70           C  
ATOM    463  C   ALA A 238      41.002  90.271  15.537  1.00 24.10           C  
ATOM    464  O   ALA A 238      41.812  89.354  15.704  1.00 26.21           O  
ATOM    465  CB  ALA A 238      41.899  92.609  15.754  1.00 22.64           C  
ATOM    466  N   ALA A 239      39.741  90.229  15.978  1.00 20.94           N  
ATOM    467  CA  ALA A 239      39.190  89.066  16.679  1.00 20.86           C  
ATOM    468  C   ALA A 239      39.071  87.898  15.705  1.00 17.91           C  
ATOM    469  O   ALA A 239      39.429  86.777  16.038  1.00 23.27           O  
ATOM    470  CB  ALA A 239      37.832  89.387  17.283  1.00 16.11           C  
ATOM    471  N   ARG A 240      38.618  88.172  14.484  1.00 22.62           N  
ATOM    472  CA  ARG A 240      38.473  87.139  13.447  1.00 21.48           C  
ATOM    473  C   ARG A 240      39.830  86.467  13.145  1.00 19.54           C  
ATOM    474  O   ARG A 240      39.938  85.234  13.100  1.00 21.32           O  
ATOM    475  CB  ARG A 240      37.889  87.762  12.172  1.00 22.15           C  
ATOM    476  CG  ARG A 240      37.144  86.787  11.280  1.00 25.38           C  
ATOM    477  CD  ARG A 240      36.789  87.382   9.898  1.00 24.63           C  
ATOM    478  NE  ARG A 240      35.966  88.581   9.986  1.00 27.69           N  
ATOM    479  CZ  ARG A 240      34.719  88.606  10.445  1.00 29.10           C  
ATOM    480  NH1 ARG A 240      34.131  87.489  10.851  1.00 29.02           N  
ATOM    481  NH2 ARG A 240      34.074  89.759  10.546  1.00 27.44           N  
ATOM    482  N   ARG A 241      40.867  87.282  12.966  1.00 22.10           N  
ATOM    483  CA  ARG A 241      42.213  86.776  12.693  1.00 22.19           C  
ATOM    484  C   ARG A 241      42.765  85.982  13.871  1.00 24.03           C  
ATOM    485  O   ARG A 241      43.412  84.951  13.675  1.00 25.44           O  
ATOM    486  CB  ARG A 241      43.161  87.929  12.367  1.00 20.10           C  
ATOM    487  CG  ARG A 241      42.712  88.747  11.178  1.00 26.46           C  
ATOM    488  CD  ARG A 241      43.814  89.654  10.672  1.00 30.41           C  
ATOM    489  NE  ARG A 241      44.136  90.731  11.606  1.00 33.12           N  
ATOM    490  CZ  ARG A 241      43.615  91.954  11.544  1.00 32.79           C  
ATOM    491  NH1 ARG A 241      42.731  92.266  10.596  1.00 27.64           N  
ATOM    492  NH2 ARG A 241      44.012  92.883  12.403  1.00 32.60           N  
ATOM    493  N   SER A 242      42.507  86.471  15.088  1.00 27.23           N  
ATOM    494  CA  SER A 242      42.958  85.825  16.325  1.00 24.50           C  
ATOM    495  C   SER A 242      42.319  84.443  16.498  1.00 25.77           C  
ATOM    496  O   SER A 242      43.016  83.474  16.832  1.00 30.22           O  
ATOM    497  CB  SER A 242      42.647  86.714  17.535  1.00 29.54           C  
ATOM    498  OG  SER A 242      43.349  86.296  18.693  1.00 27.15           O  
ATOM    499  N   ARG A 243      41.008  84.340  16.265  1.00 21.30           N  
ATOM    500  CA  ARG A 243      40.314  83.055  16.375  1.00 21.49           C  
ATOM    501  C   ARG A 243      40.889  82.050  15.383  1.00 23.33           C  
ATOM    502  O   ARG A 243      41.065  80.867  15.688  1.00 21.40           O  
ATOM    503  CB AARG A 243      38.832  83.199  16.047  0.50 24.39           C  
ATOM    504  CB BARG A 243      38.814  83.231  16.151  0.50 21.46           C  
ATOM    505  CG AARG A 243      38.024  84.126  16.917  0.50 27.08           C  
ATOM    506  CG BARG A 243      38.114  84.006  17.258  0.50 17.97           C  
ATOM    507  CD AARG A 243      36.575  84.048  16.465  0.50 29.72           C  
ATOM    508  CD BARG A 243      36.597  83.890  17.148  0.50 20.57           C  
ATOM    509  NE AARG A 243      35.806  85.231  16.827  0.50 34.37           N  
ATOM    510  NE BARG A 243      36.044  84.538  15.960  0.50 19.21           N  
ATOM    511  CZ AARG A 243      35.264  86.073  15.952  0.50 38.16           C  
ATOM    512  CZ BARG A 243      35.548  85.773  15.938  0.50 22.85           C  
ATOM    513  NH1AARG A 243      35.396  85.882  14.644  0.50 36.69           N  
ATOM    514  NH1BARG A 243      35.539  86.508  17.044  0.50 17.31           N  
ATOM    515  NH2AARG A 243      34.587  87.117  16.391  0.50 37.75           N  
ATOM    516  NH2BARG A 243      35.035  86.264  14.812  0.50 17.70           N  
ATOM    517  N   ALA A 244      41.141  82.527  14.173  1.00 28.41           N  
ATOM    518  CA  ALA A 244      41.693  81.697  13.117  1.00 28.14           C  
ATOM    519  C   ALA A 244      43.045  81.106  13.522  1.00 30.36           C  
ATOM    520  O   ALA A 244      43.330  79.940  13.231  1.00 32.38           O  
ATOM    521  CB  ALA A 244      41.821  82.508  11.835  1.00 26.54           C  
ATOM    522  N   ARG A 245      43.883  81.912  14.170  1.00 30.83           N  
ATOM    523  CA  ARG A 245      45.189  81.440  14.620  1.00 29.36           C  
ATOM    524  C   ARG A 245      45.030  80.372  15.700  1.00 29.79           C  
ATOM    525  O   ARG A 245      45.744  79.371  15.696  1.00 29.58           O  
ATOM    526  CB  ARG A 245      46.032  82.593  15.153  1.00 30.82           C  
ATOM    527  CG  ARG A 245      46.380  83.641  14.121  1.00 32.79           C  
ATOM    528  CD  ARG A 245      47.240  84.742  14.720  1.00 33.45           C  
ATOM    529  NE  ARG A 245      47.091  85.978  13.962  1.00 40.06           N  
ATOM    530  CZ  ARG A 245      46.634  87.119  14.471  1.00 44.74           C  
ATOM    531  NH1 ARG A 245      46.289  87.195  15.750  1.00 37.62           N  
ATOM    532  NH2 ARG A 245      46.475  88.177  13.686  1.00 53.16           N  
ATOM    533  N   LYS A 246      44.082  80.574  16.612  1.00 32.38           N  
ATOM    534  CA  LYS A 246      43.830  79.614  17.684  1.00 33.08           C  
ATOM    535  C   LYS A 246      43.311  78.273  17.151  1.00 32.93           C  
ATOM    536  O   LYS A 246      43.555  77.227  17.759  1.00 32.93           O  
ATOM    537  CB  LYS A 246      42.842  80.177  18.717  1.00 33.25           C  
ATOM    538  CG  LYS A 246      43.359  81.375  19.489  1.00 44.64           C  
ATOM    539  CD  LYS A 246      42.406  81.784  20.612  1.00 53.26           C  
ATOM    540  CE  LYS A 246      41.292  82.734  20.146  1.00 58.39           C  
ATOM    541  NZ  LYS A 246      41.772  84.143  19.966  1.00 57.74           N  
ATOM    542  N   LEU A 247      42.579  78.301  16.040  1.00 28.91           N  
ATOM    543  CA  LEU A 247      42.052  77.073  15.449  1.00 29.11           C  
ATOM    544  C   LEU A 247      43.161  76.259  14.777  1.00 31.82           C  
ATOM    545  O   LEU A 247      43.165  75.027  14.840  1.00 34.13           O  
ATOM    546  CB  LEU A 247      40.963  77.392  14.430  1.00 33.43           C  
ATOM    547  CG  LEU A 247      39.801  76.405  14.308  1.00 33.28           C  
ATOM    548  CD1 LEU A 247      38.913  76.851  13.172  1.00 41.52           C  
ATOM    549  CD2 LEU A 247      40.285  74.996  14.065  1.00 32.76           C  
ATOM    550  N   GLN A 248      44.101  76.944  14.134  1.00 32.96           N  
ATOM    551  CA  GLN A 248      45.206  76.267  13.476  1.00 36.66           C  
ATOM    552  C   GLN A 248      46.211  75.741  14.505  1.00 35.00           C  
ATOM    553  O   GLN A 248      46.793  74.667  14.324  1.00 34.38           O  
ATOM    554  CB  GLN A 248      45.899  77.188  12.468  1.00 47.93           C  
ATOM    555  CG  GLN A 248      46.685  78.329  13.094  1.00 61.64           C  
ATOM    556  CD  GLN A 248      47.589  79.047  12.105  1.00 67.40           C  
ATOM    557  OE1 GLN A 248      48.753  79.326  12.408  1.00 71.39           O  
ATOM    558  NE2 GLN A 248      47.058  79.362  10.924  1.00 64.32           N  
ATOM    559  N   ARG A 249      46.429  76.506  15.572  1.00 31.49           N  
ATOM    560  CA  ARG A 249      47.347  76.089  16.631  1.00 31.89           C  
ATOM    561  C   ARG A 249      46.862  74.785  17.259  1.00 27.88           C  
ATOM    562  O   ARG A 249      47.653  73.875  17.479  1.00 28.65           O  
ATOM    563  CB  ARG A 249      47.482  77.180  17.699  1.00 34.39           C  
ATOM    564  CG  ARG A 249      48.275  78.403  17.242  1.00 46.52           C  
ATOM    565  CD  ARG A 249      48.392  79.462  18.349  1.00 56.14           C  
ATOM    566  NE  ARG A 249      47.542  80.633  18.116  1.00 59.60           N  
ATOM    567  CZ  ARG A 249      46.973  81.361  19.076  1.00 58.69           C  
ATOM    568  NH1 ARG A 249      47.144  81.050  20.353  1.00 58.53           N  
ATOM    569  NH2 ARG A 249      46.239  82.419  18.755  1.00 63.15           N  
ATOM    570  N   MET A 250      45.557  74.690  17.500  1.00 24.94           N  
ATOM    571  CA  MET A 250      44.950  73.503  18.077  1.00 24.54           C  
ATOM    572  C   MET A 250      45.197  72.290  17.183  1.00 31.22           C  
ATOM    573  O   MET A 250      45.632  71.236  17.661  1.00 30.50           O  
ATOM    574  CB AMET A 250      43.446  73.700  18.261  0.50 26.40           C  
ATOM    575  CB BMET A 250      43.452  73.728  18.219  0.50 29.12           C  
ATOM    576  CG AMET A 250      42.760  72.581  19.021  0.50 27.79           C  
ATOM    577  CG BMET A 250      42.718  72.570  18.833  0.50 33.16           C  
ATOM    578  SD AMET A 250      43.327  72.407  20.730  0.50 35.90           S  
ATOM    579  SD BMET A 250      40.998  72.558  18.315  0.50 47.85           S  
ATOM    580  CE AMET A 250      42.272  71.112  21.307  0.50 31.87           C  
ATOM    581  CE BMET A 250      40.482  74.207  18.795  0.50 38.70           C  
ATOM    582  N   LYS A 251      44.909  72.436  15.887  1.00 33.62           N  
ATOM    583  CA  LYS A 251      45.100  71.353  14.909  1.00 33.31           C  
ATOM    584  C   LYS A 251      46.556  70.926  14.798  1.00 27.11           C  
ATOM    585  O   LYS A 251      46.861  69.737  14.766  1.00 25.20           O  
ATOM    586  CB  LYS A 251      44.537  71.761  13.539  1.00 43.00           C  
ATOM    587  CG  LYS A 251      43.010  71.824  13.513  1.00 49.89           C  
ATOM    588  CD  LYS A 251      42.457  72.083  12.122  1.00 57.43           C  
ATOM    589  CE  LYS A 251      42.803  73.482  11.638  1.00 65.63           C  
ATOM    590  NZ  LYS A 251      42.070  73.852  10.389  1.00 72.28           N  
ATOM    591  N   GLN A 252      47.444  71.910  14.760  1.00 26.17           N  
ATOM    592  CA  GLN A 252      48.873  71.686  14.702  1.00 29.65           C  
ATOM    593  C   GLN A 252      49.257  70.801  15.887  1.00 34.67           C  
ATOM    594  O   GLN A 252      49.905  69.757  15.728  1.00 35.26           O  
ATOM    595  CB  GLN A 252      49.583  73.036  14.806  1.00 40.22           C  
ATOM    596  CG  GLN A 252      51.084  72.988  15.090  1.00 55.81           C  
ATOM    597  CD  GLN A 252      51.577  74.250  15.795  1.00 65.21           C  
ATOM    598  OE1 GLN A 252      51.911  74.222  16.982  1.00 71.27           O  
ATOM    599  NE2 GLN A 252      51.600  75.366  15.073  1.00 68.43           N  
ATOM    600  N   LEU A 253      48.814  71.217  17.070  1.00 37.96           N  
ATOM    601  CA  LEU A 253      49.070  70.513  18.326  1.00 32.95           C  
ATOM    602  C   LEU A 253      48.505  69.092  18.299  1.00 30.53           C  
ATOM    603  O   LEU A 253      49.181  68.149  18.691  1.00 30.83           O  
ATOM    604  CB  LEU A 253      48.452  71.301  19.484  1.00 34.41           C  
ATOM    605  CG  LEU A 253      48.851  70.922  20.904  1.00 40.51           C  
ATOM    606  CD1 LEU A 253      50.350  71.056  21.032  1.00 41.41           C  
ATOM    607  CD2 LEU A 253      48.146  71.819  21.910  1.00 38.34           C  
ATOM    608  N   GLU A 254      47.278  68.933  17.814  1.00 29.41           N  
ATOM    609  CA  GLU A 254      46.665  67.613  17.743  1.00 31.13           C  
ATOM    610  C   GLU A 254      47.447  66.664  16.838  1.00 33.27           C  
ATOM    611  O   GLU A 254      47.565  65.477  17.147  1.00 32.31           O  
ATOM    612  CB  GLU A 254      45.218  67.715  17.276  1.00 34.52           C  
ATOM    613  CG  GLU A 254      44.360  68.567  18.181  1.00 44.41           C  
ATOM    614  CD  GLU A 254      42.922  68.611  17.737  1.00 49.62           C  
ATOM    615  OE1 GLU A 254      42.151  67.741  18.190  1.00 57.49           O  
ATOM    616  OE2 GLU A 254      42.562  69.507  16.940  1.00 53.94           O  
ATOM    617  N   ASP A 255      47.983  67.191  15.733  1.00 33.34           N  
ATOM    618  CA  ASP A 255      48.772  66.398  14.786  1.00 32.54           C  
ATOM    619  C   ASP A 255      50.071  65.927  15.432  1.00 33.65           C  
ATOM    620  O   ASP A 255      50.511  64.791  15.215  1.00 33.89           O  
ATOM    621  CB  ASP A 255      49.127  67.212  13.531  1.00 32.78           C  
ATOM    622  CG  ASP A 255      47.977  67.311  12.529  1.00 29.75           C  
ATOM    623  OD1 ASP A 255      47.093  66.428  12.492  1.00 25.92           O  
ATOM    624  OD2 ASP A 255      47.983  68.287  11.758  1.00 27.62           O  
ATOM    625  N   LYS A 256      50.687  66.819  16.207  1.00 32.91           N  
ATOM    626  CA  LYS A 256      51.943  66.533  16.896  1.00 30.58           C  
ATOM    627  C   LYS A 256      51.821  65.354  17.856  1.00 28.93           C  
ATOM    628  O   LYS A 256      52.703  64.495  17.914  1.00 29.34           O  
ATOM    629  CB  LYS A 256      52.418  67.771  17.652  1.00 30.23           C  
ATOM    630  CG  LYS A 256      53.820  67.661  18.215  1.00 37.76           C  
ATOM    631  CD  LYS A 256      54.852  67.481  17.113  1.00 46.30           C  
ATOM    632  CE  LYS A 256      56.262  67.541  17.671  1.00 51.02           C  
ATOM    633  NZ  LYS A 256      56.487  68.816  18.424  1.00 55.52           N  
ATOM    634  N   VAL A 257      50.721  65.311  18.597  1.00 28.55           N  
ATOM    635  CA  VAL A 257      50.480  64.228  19.542  1.00 31.77           C  
ATOM    636  C   VAL A 257      50.363  62.921  18.768  1.00 31.72           C  
ATOM    637  O   VAL A 257      50.835  61.875  19.216  1.00 35.79           O  
ATOM    638  CB  VAL A 257      49.173  64.461  20.369  1.00 29.18           C  
ATOM    639  CG1 VAL A 257      48.868  63.246  21.238  1.00 26.30           C  
ATOM    640  CG2 VAL A 257      49.317  65.693  21.252  1.00 29.43           C  
ATOM    641  N   GLU A 258      49.766  62.995  17.584  1.00 31.42           N  
ATOM    642  CA  GLU A 258      49.572  61.826  16.735  1.00 30.17           C  
ATOM    643  C   GLU A 258      50.923  61.343  16.213  1.00 26.46           C  
ATOM    644  O   GLU A 258      51.217  60.148  16.224  1.00 26.98           O  
ATOM    645  CB  GLU A 258      48.639  62.186  15.572  1.00 35.61           C  
ATOM    646  CG  GLU A 258      48.004  60.991  14.872  1.00 48.69           C  
ATOM    647  CD  GLU A 258      47.147  61.385  13.673  1.00 54.21           C  
ATOM    648  OE1 GLU A 258      46.134  62.091  13.876  1.00 53.51           O  
ATOM    649  OE2 GLU A 258      47.483  60.978  12.534  1.00 50.36           O  
ATOM    650  N   GLU A 259      51.749  62.296  15.792  1.00 25.32           N  
ATOM    651  CA  GLU A 259      53.077  62.028  15.266  1.00 22.89           C  
ATOM    652  C   GLU A 259      53.983  61.413  16.333  1.00 24.99           C  
ATOM    653  O   GLU A 259      54.662  60.416  16.071  1.00 23.16           O  
ATOM    654  CB  GLU A 259      53.668  63.334  14.734  1.00 25.70           C  
ATOM    655  CG  GLU A 259      54.949  63.195  13.944  1.00 38.83           C  
ATOM    656  CD  GLU A 259      56.183  63.142  14.817  1.00 48.96           C  
ATOM    657  OE1 GLU A 259      56.603  64.201  15.339  1.00 54.33           O  
ATOM    658  OE2 GLU A 259      56.739  62.036  14.979  1.00 57.46           O  
ATOM    659  N   LEU A 260      53.989  62.003  17.531  1.00 23.86           N  
ATOM    660  CA  LEU A 260      54.810  61.516  18.646  1.00 22.30           C  
ATOM    661  C   LEU A 260      54.350  60.159  19.169  1.00 21.23           C  
ATOM    662  O   LEU A 260      55.166  59.321  19.537  1.00 23.46           O  
ATOM    663  CB  LEU A 260      54.869  62.550  19.782  1.00 19.89           C  
ATOM    664  CG  LEU A 260      55.704  63.800  19.494  1.00 16.31           C  
ATOM    665  CD1 LEU A 260      55.458  64.872  20.528  1.00 21.80           C  
ATOM    666  CD2 LEU A 260      57.163  63.431  19.445  1.00 21.10           C  
ATOM    667  N   LEU A 261      53.050  59.919  19.178  1.00 19.06           N  
ATOM    668  CA  LEU A 261      52.545  58.635  19.627  1.00 24.28           C  
ATOM    669  C   LEU A 261      53.105  57.517  18.733  1.00 28.50           C  
ATOM    670  O   LEU A 261      53.548  56.473  19.232  1.00 30.49           O  
ATOM    671  CB  LEU A 261      51.014  58.648  19.602  1.00 28.55           C  
ATOM    672  CG  LEU A 261      50.193  58.495  20.892  1.00 26.74           C  
ATOM    673  CD1 LEU A 261      50.957  58.888  22.111  1.00 28.17           C  
ATOM    674  CD2 LEU A 261      48.950  59.327  20.787  1.00 25.87           C  
ATOM    675  N   SER A 262      53.135  57.758  17.418  1.00 30.64           N  
ATOM    676  CA  SER A 262      53.646  56.779  16.448  1.00 28.69           C  
ATOM    677  C   SER A 262      55.163  56.621  16.520  1.00 25.06           C  
ATOM    678  O   SER A 262      55.688  55.505  16.461  1.00 24.35           O  
ATOM    679  CB  SER A 262      53.221  57.139  15.011  1.00 35.33           C  
ATOM    680  OG  SER A 262      54.061  58.126  14.420  1.00 46.49           O  
ATOM    681  N   LYS A 263      55.876  57.736  16.606  1.00 21.08           N  
ATOM    682  CA  LYS A 263      57.319  57.682  16.706  1.00 24.40           C  
ATOM    683  C   LYS A 263      57.671  56.910  17.981  1.00 24.13           C  
ATOM    684  O   LYS A 263      58.563  56.069  17.982  1.00 28.50           O  
ATOM    685  CB  LYS A 263      57.900  59.092  16.742  1.00 26.61           C  
ATOM    686  CG  LYS A 263      59.404  59.127  16.526  1.00 39.77           C  
ATOM    687  CD  LYS A 263      59.906  60.545  16.247  1.00 49.71           C  
ATOM    688  CE  LYS A 263      59.578  61.008  14.826  1.00 48.01           C  
ATOM    689  NZ  LYS A 263      59.807  62.471  14.651  1.00 44.29           N  
ATOM    690  N   ASN A 264      56.915  57.160  19.045  1.00 25.53           N  
ATOM    691  CA  ASN A 264      57.105  56.504  20.341  1.00 26.95           C  
ATOM    692  C   ASN A 264      56.980  54.992  20.206  1.00 28.04           C  
ATOM    693  O   ASN A 264      57.843  54.256  20.688  1.00 29.57           O  
ATOM    694  CB AASN A 264      56.093  57.054  21.367  0.50 30.94           C  
ATOM    695  CB BASN A 264      56.057  57.005  21.333  0.50 25.93           C  
ATOM    696  CG AASN A 264      56.220  56.406  22.748  0.50 34.18           C  
ATOM    697  CG BASN A 264      56.659  57.786  22.470  0.50 27.01           C  
ATOM    698  OD1AASN A 264      55.268  55.815  23.253  0.50 35.05           O  
ATOM    699  OD1BASN A 264      57.588  58.580  22.277  0.50 19.70           O  
ATOM    700  ND2AASN A 264      57.373  56.564  23.383  0.50 38.12           N  
ATOM    701  ND2BASN A 264      56.134  57.567  23.674  0.50 23.58           N  
ATOM    702  N   TYR A 265      55.923  54.535  19.529  1.00 29.39           N  
ATOM    703  CA  TYR A 265      55.667  53.105  19.328  1.00 26.09           C  
ATOM    704  C   TYR A 265      56.795  52.398  18.591  1.00 26.52           C  
ATOM    705  O   TYR A 265      57.200  51.294  18.958  1.00 28.03           O  
ATOM    706  CB  TYR A 265      54.351  52.887  18.574  1.00 37.11           C  
ATOM    707  CG  TYR A 265      53.897  51.430  18.525  1.00 51.63           C  
ATOM    708  CD1 TYR A 265      54.478  50.513  17.637  1.00 55.84           C  
ATOM    709  CD2 TYR A 265      52.885  50.969  19.370  1.00 53.51           C  
ATOM    710  CE1 TYR A 265      54.067  49.174  17.604  1.00 59.04           C  
ATOM    711  CE2 TYR A 265      52.468  49.637  19.342  1.00 58.33           C  
ATOM    712  CZ  TYR A 265      53.057  48.745  18.458  1.00 60.61           C  
ATOM    713  OH  TYR A 265      52.627  47.429  18.435  1.00 60.82           O  
ATOM    714  N   HIS A 266      57.281  53.010  17.523  1.00 31.26           N  
ATOM    715  CA  HIS A 266      58.364  52.431  16.758  1.00 32.16           C  
ATOM    716  C   HIS A 266      59.649  52.318  17.591  1.00 31.04           C  
ATOM    717  O   HIS A 266      60.368  51.323  17.486  1.00 31.74           O  
ATOM    718  CB  HIS A 266      58.592  53.227  15.469  1.00 38.78           C  
ATOM    719  CG  HIS A 266      57.430  53.189  14.520  1.00 54.37           C  
ATOM    720  ND1 HIS A 266      56.579  52.109  14.411  1.00 56.84           N  
ATOM    721  CD2 HIS A 266      56.978  54.104  13.617  1.00 57.33           C  
ATOM    722  CE1 HIS A 266      55.662  52.352  13.490  1.00 53.73           C  
ATOM    723  NE2 HIS A 266      55.886  53.556  12.997  1.00 53.96           N  
ATOM    724  N   LEU A 267      59.936  53.314  18.428  1.00 27.49           N  
ATOM    725  CA  LEU A 267      61.131  53.270  19.274  1.00 26.39           C  
ATOM    726  C   LEU A 267      60.974  52.232  20.383  1.00 28.71           C  
ATOM    727  O   LEU A 267      61.901  51.486  20.689  1.00 30.67           O  
ATOM    728  CB  LEU A 267      61.420  54.632  19.900  1.00 26.61           C  
ATOM    729  CG  LEU A 267      61.887  55.799  19.032  1.00 26.77           C  
ATOM    730  CD1 LEU A 267      62.065  57.017  19.912  1.00 29.06           C  
ATOM    731  CD2 LEU A 267      63.187  55.473  18.327  1.00 25.55           C  
ATOM    732  N   GLU A 268      59.788  52.170  20.976  1.00 33.97           N  
ATOM    733  CA  GLU A 268      59.514  51.212  22.039  1.00 35.68           C  
ATOM    734  C   GLU A 268      59.675  49.796  21.501  1.00 39.18           C  
ATOM    735  O   GLU A 268      60.242  48.920  22.159  1.00 41.44           O  
ATOM    736  CB  GLU A 268      58.099  51.413  22.578  1.00 35.45           C  
ATOM    737  CG  GLU A 268      57.901  50.872  23.974  1.00 42.76           C  
ATOM    738  CD  GLU A 268      58.685  51.641  25.024  1.00 45.94           C  
ATOM    739  OE1 GLU A 268      58.200  52.704  25.461  1.00 44.88           O  
ATOM    740  OE2 GLU A 268      59.781  51.185  25.419  1.00 48.77           O  
ATOM    741  N   ASN A 269      59.209  49.582  20.279  1.00 41.77           N  
ATOM    742  CA  ASN A 269      59.304  48.277  19.641  1.00 45.21           C  
ATOM    743  C   ASN A 269      60.767  47.999  19.285  1.00 46.57           C  
ATOM    744  O   ASN A 269      61.268  46.881  19.454  1.00 44.72           O  
ATOM    745  CB  ASN A 269      58.426  48.265  18.387  1.00 53.13           C  
ATOM    746  CG  ASN A 269      57.796  46.913  18.132  1.00 57.13           C  
ATOM    747  OD1 ASN A 269      58.241  46.165  17.255  1.00 63.82           O  
ATOM    748  ND2 ASN A 269      56.741  46.598  18.879  1.00 52.89           N  
ATOM    749  N   GLU A 270      61.450  49.041  18.817  1.00 46.90           N  
ATOM    750  CA  GLU A 270      62.859  48.966  18.451  1.00 42.88           C  
ATOM    751  C   GLU A 270      63.711  48.574  19.655  1.00 40.45           C  
ATOM    752  O   GLU A 270      64.615  47.741  19.540  1.00 37.38           O  
ATOM    753  CB  GLU A 270      63.320  50.314  17.879  1.00 43.74           C  
ATOM    754  CG  GLU A 270      64.805  50.588  18.031  1.00 48.79           C  
ATOM    755  CD  GLU A 270      65.537  50.684  16.713  1.00 51.86           C  
ATOM    756  OE1 GLU A 270      66.010  49.636  16.211  1.00 53.99           O  
ATOM    757  OE2 GLU A 270      65.661  51.815  16.194  1.00 52.60           O  
ATOM    758  N   VAL A 271      63.407  49.164  20.810  1.00 36.95           N  
ATOM    759  CA  VAL A 271      64.141  48.878  22.040  1.00 38.04           C  
ATOM    760  C   VAL A 271      64.014  47.401  22.406  1.00 40.72           C  
ATOM    761  O   VAL A 271      65.010  46.743  22.699  1.00 41.03           O  
ATOM    762  CB  VAL A 271      63.680  49.802  23.213  1.00 33.65           C  
ATOM    763  CG1 VAL A 271      63.959  49.163  24.562  1.00 28.90           C  
ATOM    764  CG2 VAL A 271      64.412  51.126  23.134  1.00 29.92           C  
ATOM    765  N   ALA A 272      62.796  46.872  22.331  1.00 44.61           N  
ATOM    766  CA  ALA A 272      62.547  45.469  22.642  1.00 42.60           C  
ATOM    767  C   ALA A 272      63.393  44.559  21.748  1.00 44.30           C  
ATOM    768  O   ALA A 272      64.004  43.597  22.223  1.00 44.19           O  
ATOM    769  CB  ALA A 272      61.070  45.156  22.467  1.00 42.92           C  
ATOM    770  N   ARG A 273      63.457  44.901  20.463  1.00 45.26           N  
ATOM    771  CA  ARG A 273      64.214  44.133  19.482  1.00 44.32           C  
ATOM    772  C   ARG A 273      65.713  44.131  19.792  1.00 48.67           C  
ATOM    773  O   ARG A 273      66.316  43.063  19.958  1.00 49.80           O  
ATOM    774  CB AARG A 273      63.984  44.717  18.084  0.50 41.27           C  
ATOM    775  CB BARG A 273      63.935  44.646  18.066  0.50 44.10           C  
ATOM    776  CG AARG A 273      64.484  43.848  16.936  0.50 41.02           C  
ATOM    777  CG BARG A 273      62.447  44.634  17.704  0.50 46.46           C  
ATOM    778  CD AARG A 273      64.292  44.527  15.573  0.50 36.12           C  
ATOM    779  CD BARG A 273      62.192  44.740  16.200  0.50 47.84           C  
ATOM    780  NE AARG A 273      65.396  45.424  15.242  0.50 32.09           N  
ATOM    781  NE BARG A 273      62.667  45.993  15.611  0.50 45.61           N  
ATOM    782  CZ AARG A 273      66.380  45.121  14.398  0.50 30.95           C  
ATOM    783  CZ BARG A 273      61.925  47.088  15.472  0.50 44.72           C  
ATOM    784  NH1AARG A 273      66.405  43.945  13.782  0.50 27.45           N  
ATOM    785  NH1BARG A 273      60.663  47.103  15.884  0.50 43.36           N  
ATOM    786  NH2AARG A 273      67.367  45.983  14.200  0.50 31.44           N  
ATOM    787  NH2BARG A 273      62.445  48.169  14.906  0.50 39.65           N  
ATOM    788  N   LEU A 274      66.307  45.319  19.901  1.00 51.46           N  
ATOM    789  CA  LEU A 274      67.735  45.450  20.200  1.00 51.82           C  
ATOM    790  C   LEU A 274      68.073  44.815  21.538  1.00 55.45           C  
ATOM    791  O   LEU A 274      69.156  44.269  21.713  1.00 57.15           O  
ATOM    792  CB  LEU A 274      68.160  46.916  20.217  1.00 51.30           C  
ATOM    793  CG  LEU A 274      68.442  47.602  18.878  1.00 52.76           C  
ATOM    794  CD1 LEU A 274      68.440  49.111  19.071  1.00 51.66           C  
ATOM    795  CD2 LEU A 274      69.768  47.129  18.314  1.00 48.66           C  
ATOM    796  N   LYS A 275      67.146  44.906  22.484  1.00 58.31           N  
ATOM    797  CA  LYS A 275      67.341  44.321  23.799  1.00 58.92           C  
ATOM    798  C   LYS A 275      67.615  42.837  23.594  1.00 62.70           C  
ATOM    799  O   LYS A 275      68.628  42.323  24.064  1.00 66.23           O  
ATOM    800  CB  LYS A 275      66.081  44.494  24.646  1.00 59.02           C  
ATOM    801  CG  LYS A 275      66.338  44.939  26.067  1.00 63.27           C  
ATOM    802  CD  LYS A 275      66.877  46.356  26.103  1.00 67.14           C  
ATOM    803  CE  LYS A 275      67.163  46.812  27.531  1.00 76.24           C  
ATOM    804  NZ  LYS A 275      67.682  48.219  27.610  1.00 78.46           N  
ATOM    805  N   LYS A 276      66.732  42.167  22.851  1.00 64.79           N  
ATOM    806  CA  LYS A 276      66.871  40.734  22.575  1.00 65.76           C  
ATOM    807  C   LYS A 276      68.200  40.411  21.885  1.00 66.59           C  
ATOM    808  O   LYS A 276      68.998  39.607  22.387  1.00 65.36           O  
ATOM    809  CB  LYS A 276      65.698  40.237  21.728  1.00 62.50           C  
ATOM    810  N   LEU A 277      68.417  41.020  20.723  1.00 66.99           N  
ATOM    811  CA  LEU A 277      69.643  40.812  19.967  1.00 66.22           C  
ATOM    812  C   LEU A 277      70.787  41.566  20.645  1.00 68.17           C  
ATOM    813  O   LEU A 277      71.175  41.256  21.774  1.00 69.45           O  
ATOM    814  CB  LEU A 277      69.467  41.292  18.532  1.00 62.84           C  
TER     815      LEU A 277                                                      
HETATM  816  O   HOH B  10      34.994  82.355  19.501  1.00 49.83           O  
HETATM  817  O   HOH B  11      26.431  72.666  16.705  1.00 72.16           O  
HETATM  818  O   HOH B  12      48.001 100.342  27.919  1.00 58.53           O  
HETATM  819  O   HOH B  13      18.053  91.147  11.274  1.00 64.62           O  
HETATM  820  O   HOH B  14      28.240  82.538  13.880  1.00 40.66           O  
HETATM  821  O   HOH B  15      35.684  80.729  15.343  1.00 69.32           O  
HETATM  822  O   HOH B  16      14.000  58.797  12.895  1.00 58.59           O  
HETATM  823  O   HOH B  17      42.161  98.516  30.978  1.00 59.49           O  
HETATM  824  O   HOH B  18      44.219 100.752  26.909  1.00 56.20           O  
HETATM  825  O   HOH B  19      41.135  99.354  23.346  1.00 53.99           O  
HETATM  826  O   HOH B  20      25.423  68.279  20.445  1.00 51.52           O  
HETATM  827  O   HOH B  21      54.049 104.089  18.042  1.00 56.02           O  
HETATM  828  O   HOH B  22      17.797  73.905  21.692  1.00 45.97           O  
HETATM  829  O   HOH B  23      27.969  88.274  17.371  1.00 69.46           O  
HETATM  830  O   HOH B  24      30.372  92.924  11.516  1.00 53.44           O  
HETATM  831  O   HOH B  25      34.589  89.048  14.459  1.00 22.47           O  
HETATM  832  O   HOH B  26      35.902  85.970  19.723  1.00 40.17           O  
HETATM  833  O   HOH B  27      57.064 101.960  16.076  1.00 58.73           O  
HETATM  834  O   HOH B  28      40.428  92.027  29.606  1.00 51.70           O  
HETATM  835  O   HOH B  29      31.698  96.593  13.623  1.00 46.51           O  
HETATM  836  O   HOH B  30      37.432  84.152  21.070  1.00 59.50           O  
HETATM  837  O   HOH B  31      38.531  88.954  20.249  1.00 22.27           O  
HETATM  838  O   HOH B  32      26.632  70.645  19.615  1.00 33.59           O  
HETATM  839  O   HOH B  33      30.862  89.627   9.031  1.00 45.53           O  
HETATM  840  O   HOH A   5      50.295  70.822  11.179  1.00 52.68           O  
HETATM  841  O   HOH A   9      34.860  95.023  18.729  1.00 41.44           O  
HETATM  842  O   HOH A  14      44.307  76.657  20.310  1.00 39.79           O  
HETATM  843  O   HOH A  16      43.917  84.683  10.506  1.00 45.65           O  
HETATM  844  O   HOH A  18      29.463 100.976  13.357  1.00 73.22           O  
HETATM  845  O   HOH A  19      41.900  95.066  12.025  1.00 29.47           O  
HETATM  846  O   HOH A  20      39.674  72.494   9.733  1.00 64.06           O  
HETATM  847  O   HOH A  21      44.437  89.465  15.371  1.00 35.50           O  
HETATM  848  O   HOH A  23      56.136  57.829  12.659  1.00 32.16           O  
HETATM  849  O   HOH A  25      39.046  79.362  17.731  1.00 35.73           O  
HETATM  850  O   HOH A  26      42.178  95.314  18.530  1.00 28.11           O  
HETATM  851  O   HOH A  27      42.133  78.146  11.107  1.00 42.60           O  
HETATM  852  O   HOH A  30      45.534  64.760  14.124  1.00 54.72           O  
HETATM  853  O   HOH A  32      60.433  48.022  24.653  1.00 45.59           O  
HETATM  854  O   HOH A  33      40.899  97.281  20.026  1.00 40.45           O  
HETATM  855  O   HOH A  37      40.191  86.738  20.710  1.00 36.28           O  
HETATM  856  O   HOH A  38      51.467  69.070  13.771  1.00 36.30           O  
HETATM  857  O   HOH A  39      49.492  57.946  16.214  1.00 31.19           O  
HETATM  858  O   HOH A  42      51.175  54.000  21.050  1.00 51.45           O  
HETATM  859  O   HOH A  43      32.291  97.011   8.113  1.00 56.92           O  
HETATM  860  O   HOH A  44      34.854  94.562  10.621  1.00 46.29           O  
HETATM  861  O   HOH A  46      34.865  96.265   8.218  1.00 45.93           O  
MASTER      399    0    0    1    0    0    0    6  859    2    0    7          
END                                                                             
""")
    Xponge.pdb_filter(s_in, "test_filter.pdb", ["ATOM", "TER", "SEQRES"], [], ["B"])
