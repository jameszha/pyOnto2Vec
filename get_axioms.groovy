@Grapes([
    @Grab(group="org.semanticweb.elk", module="elk-owlapi", version="0.4.3"),
    @Grab(group="net.sourceforge.owlapi", module="owlapi-api", version="4.2.5"),
    @Grab(group="net.sourceforge.owlapi", module="owlapi-apibinding", version="4.2.5"),
    @Grab(group="net.sourceforge.owlapi", module="owlapi-impl", version="4.2.5"),
    @Grab(group="net.sourceforge.owlapi", module="owlapi-parsers", version="4.2.5"),
    @Grab(group='net.sourceforge.owlapi', module='org.semanticweb.hermit', version='1.3.8.413'),
    @Grab(group ='net.sourceforge.owlapi',module='owlapi-osgidistribution',version='4.2.6'),
    @Grab(group='org.slf4j', module='slf4j-log4j12', version='1.7.10'),
    @GrabConfig(systemClassLoader=true)
])

// @Grapes ([

//     @Grab(group='org.semanticweb.elk', module='elk-owlapi', version='0.4.2'),
//     @Grab(group='net.sourceforge.owlapi', module='owlapi-api', version='4.1.0'),
//     @Grab(group='net.sourceforge.owlapi', module='owlapi-apibinding', version='4.1.0'),
//     @Grab(group='net.sourceforge.owlapi', module='owlapi-impl', version='4.1.0'),
//     @Grab(group='net.sourceforge.owlapi', module='owlapi-parsers', version='4.1.0'),
//     @Grab(group='net.sourceforge.owlapi', module='org.semanticweb.hermit', version='1.3.8.413'),
//     @Grab(group ='net.sourceforge.owlapi',module='owlapi-osgidistribution',version='4.2.6'),
//     @GrabConfig(systemClassLoader=true)
// ])

import java.io.File;
import java.util.ArrayList;
import java.util.List;

import org.semanticweb.elk.owlapi.ElkReasonerFactory;
import org.semanticweb.HermiT.Reasoner;

import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.formats.FunctionalSyntaxDocumentFormat;
import org.semanticweb.owlapi.io.OWLObjectRenderer;
import org.semanticweb.owlapi.manchestersyntax.renderer.ManchesterOWLSyntaxOWLObjectRendererImpl;
import org.semanticweb.owlapi.model.*
import org.semanticweb.owlapi.reasoner.InferenceType;
import org.semanticweb.owlapi.reasoner.OWLReasoner;
import org.semanticweb.owlapi.reasoner.OWLReasonerFactory;
import org.semanticweb.owlapi.util.InferredAxiomGenerator;
import org.semanticweb.owlapi.util.InferredDisjointClassesAxiomGenerator;
import org.semanticweb.owlapi.util.InferredEquivalentClassAxiomGenerator;
import org.semanticweb.owlapi.util.InferredOntologyGenerator;
import org.semanticweb.owlapi.util.InferredSubClassAxiomGenerator;


/**
 * get_axioms.groovy
 *
 * Convert OWL ontology into lists of axioms. Uses ELK reasoner to infer new subclass, equivalence, and disjoint axioms
 * Author: James Zhang (jameszhangxiv@gmail.com)
 *
 *
 * Modified from:
 *  "Java Code Examples for org.semanticweb.owlapi.util.InferredSubClassAxiomGenerator" 
 *  Authors: Frantisek Simancik, Pavel Klinov, Peter Skocovsky
 *  https://www.programcreek.com/java-api-examples/index.php?api=org.semanticweb.owlapi.util.InferredSubClassAxiomGenerator 
 *
 * Tested with ELK 0.4.3, OWL API 4.2.5, and Java 1.8.0_111. 
 * Using OWLReasoner.getReasonerVersion() in OWL API 4.2.9 may cause NumberFormatException.
 *
 */


/*******************************************************
 *                      LOAD
 *******************************************************/
long start_time = System.currentTimeMillis();

OWLOntologyManager manager = OWLManager.createOWLOntologyManager();

// Load ontology from file
System.out.printf("%nLoading ontology . . . %n");
String onto_file_name = args[0];
OWLOntology ont = manager.loadOntologyFromOntologyDocument(new File(onto_file_name));

// Create ELK reasoner
//OWLReasonerFactory reasoner_factory = new ElkReasonerFactory();

// OR Create HermiT reasoner
OWLReasonerFactory reasoner_factory = new Reasoner.ReasonerFactory();

OWLReasoner reasoner = reasoner_factory.createReasoner(ont);

// Classify the ontology.
System.out.printf("%nClassifying ontology . . . %n");
reasoner.precomputeInferences();


/*******************************************************
 *                      INFER
 *******************************************************/
// To generate an inferred ontology we use implementations of
// inferred axiom generators
System.out.printf("%nInferring new axioms . . . %n");
int axiom_count = ont.getAxiomCount();
System.out.printf("Original axiom count: " + axiom_count + "%n");

OWLDataFactory factory = manager.getOWLDataFactory()

InferredSubClassAxiomGenerator generator = new InferredSubClassAxiomGenerator();
InferredDisjointClassesAxiomGenerator generatordis = new  InferredDisjointClassesAxiomGenerator();
InferredEquivalentClassAxiomGenerator generatequi = new  InferredEquivalentClassAxiomGenerator();
Set<OWLAxiom> axioms = generator.createAxioms(factory, reasoner);
Set<OWLAxiom> dis_axioms=generatordis.createAxioms(factory, reasoner);
Set<OWLAxiom> equ_axioms=generatequi.createAxioms(factory, reasoner);
manager.addAxioms(ont,axioms);
manager.addAxioms(ont,dis_axioms);
manager.addAxioms(ont,equ_axioms);

axiom_count = ont.getAxiomCount();
System.out.printf("Final axiom count: " + axiom_count + "%n");

// Terminate the worker threads used by the reasoner.
reasoner.dispose();


/*******************************************************
 *                      OUTPUT
 *******************************************************/

OWLObjectRenderer renderer = new ManchesterOWLSyntaxOWLObjectRendererImpl ();

// Write out list of all classes to file
System.out.printf("%nWriting classes out to file . . . %n");
Set<OWLClass> classes = ont.getClassesInSignature();
PrintWriter pw = new PrintWriter(new FileWriter("classes.lst"));
for (OWLClass ont_class : classes) {
    ont_class_string = renderer.render(ont_class)
    pw.println(ont_class_string); 
}
pw.close();

// Write out list of all axioms (original and inferred) for each class to file
System.out.printf("%nWriting axioms out to file . . . %n");
pw = new PrintWriter(new FileWriter("axioms.lst"));
for (OWLClass ont_class : classes) {
    Set<OWLClassAxiom> class_axioms = ont.getAxioms (ont_class);
    for (OWLClassAxiom class_axiom: class_axioms) {
        class_axiom_string = renderer.render (class_axiom);
        class_axiom_string = class_axiom_string.replace('(', '').replace(')', '');
        pw.println(class_axiom_string); 
    }

}
pw.close();

long end_time = System.currentTimeMillis();
System.out.println("Time taken: " + ((end_time - start_time) / 1000F) + " seconds");
