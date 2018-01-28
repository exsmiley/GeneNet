from flask import Flask, render_template, jsonify, request
import json
app = Flask(__name__)

# config
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True


# load all of the data
with open('data/processed_pmid.json') as f:
    pmid_data = json.loads(f.read())

with open('data/nodes.json') as f:
    node_data = json.loads(f.read())

with open('data/edges.json') as f:
    edge_data = json.loads(f.read())        


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/visual')
def visual():
    return render_template('visual.html')

@app.route('/data')
def data():
    return render_template('data.html')


@app.route('/api/nodes')
def get_nodes():
    return jsonify(node_data)


@app.route('/api/edges')
def get_edges():
    return jsonify(edge_data)


@app.route('/api/all_pmids')
def get_all_pmids():
    return jsonify(pmid_data)


@app.route('/api/pmid')
def get_pmid():
    pmid = request.args.get('pmid')
    data = pmid_data[pmid]
    data['gene_expression_img'] = 'http://genecardsdata.blob.core.windows.net/rna-expression-v460/gene_expression_{}.png'.format(data['Official Symbol'])
    data['protein_expression_img'] = 'http://genecardsdata.blob.core.windows.net/protein-expression-v460/protein_expression_{}.png'.format(data['Official Symbol'])
    return jsonify(data)


@app.route('/api/more')
def get_more():
    return render_template('more.html')


if __name__ == '__main__':
    app.run()