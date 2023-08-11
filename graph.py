import json
import os
from os.path import join, exists

import pandas as pd
from tqdm import tqdm


def make_graph_from_relations_array(relations, entity_values, entity_types, min_links=1, weights=True):
    relations, entity_values, entity_types = list(relations), list(entity_values), list(entity_types)
    nodes_ = {}
    links_ = {}

    entity_values_flat = []
    for e in entity_values:
        entity_values_flat += e.split(",")
    entity_types_flat = []
    for e in entity_types:
        entity_types_flat += e.split(",")
    entity_map = {}
    for idx, value in enumerate(entity_values_flat):
        entity_map[value] = entity_types_flat[idx]

    for idx, relations in enumerate(filter(lambda r: str(r) != "nan", relations)):
        relations = relations.replace(";;", ";").replace(";->", "->").replace("; ", "")
        if ");(" in relations:
            relations = relations.split(");(")
        else:
            relations = [relations]

        for idx, relation in enumerate(relations):
            relation = relation.replace("(", "").replace(")", "")
            relation = relation.split(";")
            sent = relation[1]

            relation[0] = relation[0].split("->")
            source, target = relation[0][0], relation[0][1]
            source, target = source, target
            try:
                source_type = entity_map[source]
            except KeyError:
                source_type = "UNKNOWN"
            try:
                target_type = entity_map[target]
            except KeyError:
                target_type = "UNKNOWN"
            if source not in nodes_:
                nodes_[source] = 0
            if target not in nodes_:
                nodes_[target] = 0
            nodes_[source] += 1
            nodes_[target] += 1

            s_t = source_type + "." + source + "___" + target_type + "." + target + "***" + sent
            if s_t not in links_:
                links_[s_t] = 0
            links_[s_t] += 1

    node_max = 0
    link_max = 0

    links = []
    used_nodes = set()
    for s_t in links_:
        if links_[s_t] >= min_links:
            links.append({
                "source": s_t.split("___")[0],
                "target": s_t.split("___")[1].split("***")[0],
                "c": links_[s_t] if weights else 1,
                "sent": s_t.split("___")[1].split("***")[1]})
            used_nodes.add(s_t.split("___")[0])
            used_nodes.add(s_t.split("___")[1].split("***")[0])
            if link_max < links_[s_t]:
                link_max = links_[s_t]

    nodes = []
    for id in nodes_:
        if id in used_nodes:
            nodes.append({"id": id, "c": nodes_[id] if weights else 1})
            if node_max < nodes_[id]:
                node_max = nodes_[id]

    return {"nodes": nodes, "links": links}


def graphs_operations(graph_A, graph_B, operation="PLUS", min_links=0.01):
    links_ = {}

    # convert links of graph A to dict
    links_A = {}
    for link_A in graph_A["links"]:
        l = link_A["source"] + "___" + link_A["target"] + "***" + link_A["sent"]
        if l not in links_A:
            links_A[l] = 0
        links_A[l] += link_A["c"]

    if operation in ["PLUS", "MINUS"]:
        links_ = links_A
        # add or subtract links of graph B
        for link in graph_B["links"]:
            l = link["source"] + "___" + link["target"] + "***" + link["sent"]
            if l not in links_:
                links_[l] = 0
            if operation == "PLUS":
                links_[l] += link["c"]
            else:
                links_[l] -= link["c"]

    if operation in ["SAME", "DIFF"]:
        A_max, B_max = max(links_A.values()), max(map(lambda l: l["c"], graph_B["links"]))
        for l in links_A:
            links_A[l] = links_A[l] / A_max

        if operation == "SAME":
            for link_B in graph_B["links"]:
                l_B = link_B["source"] + "___" + link_B["target"] + "***" + link_B["sent"]
                c = link_B["c"] / B_max
                if l_B in links_A:
                    if c < links_A[l_B]:
                        links_[l_B] = c
                    else:
                        links_[l_B] = links_A[l_B]

        if operation == "DIFF":
            for link_B in graph_B["links"]:
                l_B = link_B["source"] + "___" + link_B["target"] + "***" + link_B["sent"]
                c = link_B["c"] / B_max
                if l_B in links_A and links_A[l_B] - c > 0:
                    links_[l_B] = links_A[l_B] - c

    links = []
    used_nodes = {}
    for s_t in links_:
        if links_[s_t] >= min_links:
            s = s_t.split("___")[0]
            t = s_t.split("___")[1].split("***")[0]
            sent = s_t.split("___")[1].split("***")[1]
            links.append({
                "source": s,
                "target": t,
                "c": links_[s_t],
                "sent": sent})
            if s not in used_nodes:
                used_nodes[s] = 0
            if t not in used_nodes:
                used_nodes[t] = 0
            used_nodes[s] += links_[s_t]
            used_nodes[t] += links_[s_t]
    nodes = []
    for id in used_nodes:
        nodes.append({"id": id, "c": used_nodes[id]})
    return {"nodes": nodes, "links": links}


def graphToRadial(graph):
    nodes_ = {}
    for n in graph["nodes"]:
        nodes_[n["id"]] = {"w": n["c"]}
    for l in graph["links"]:
        if "imports" not in nodes_[l["target"]]:
            nodes_[l["target"]]["imports"] = []
        nodes_[l["target"]]["imports"].append({
            "name": l["source"],
            "w": l["c"],
            "sent": l["sent"]
        })
    nodes = []
    for n_ in nodes_:
        n = nodes_[n_]
        n["name"] = n_
        nodes.append(n)
    return nodes


if __name__ == '__main__':

    dir = "data/nerel"
    src_subdir = "src"
    out_src_dir = join(dir, f"graph/{src_subdir}")
    out_d3_dir = join(dir, "graph")
    data = pd.read_csv(join(dir, "responses-train-0.csv"))

    # For each relation type
    for r in tqdm(set(data["relation_type"]), desc="Build graph per every relation type"):

        data_single_type = data[data["relation_type"] == r]

        graph = make_graph_from_relations_array(
            relations=data_single_type["relations_pretty_value"],
            entity_values=data_single_type["entity_values"],
            entity_types=data_single_type["entity_types"],
            min_links=1,
            weights=True
        )

        graph = graphs_operations(
            graph_A=graph, graph_B=graph, operation="SAME",
            # we could change this parameter in between [0.001 до 0.999]
            min_links=0.005
        )

        if not exists(out_src_dir):
            os.makedirs(out_src_dir)

        # open(join(out_dir, f"graph_force_{r}.json"), "w").write(json.dumps(graph, ensure_ascii=False).encode('utf8').decode())

        radial_src = join(out_src_dir, f"graph_radial_{r}.json")
        open(radial_src, "w").write(json.dumps(graphToRadial(graph), ensure_ascii=False).encode('utf8').decode())

        html_out_filepath = join(out_d3_dir, f"graph_radial_{r}.html")
        with open("data/vis_graphRadial.html", "r") as f_in:
            html_content = f_in.read()
            src_radial_filepath = join(src_subdir, f"graph_radial_{r}.json")
            html_content = html_content.replace("<SOURCE_JSON_FILEPATH>", src_radial_filepath)
            with open(html_out_filepath, "w") as f_out:
                f_out.write(html_content)
            