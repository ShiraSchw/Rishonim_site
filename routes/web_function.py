from collections import defaultdict


def build_rishonim_category_tree(rishonim):
    tree = lambda: defaultdict(tree)
    root = tree()

    for r in rishonim:
        main = r['main_category']
        sub = r['sub_category']
        sub_sub = r['sub_sub_category']
        sub_sub_sub = r.get('sub_sub_sub_category', None)

        if sub_sub_sub:
            root[main][sub][sub_sub][sub_sub_sub] = {}
        else:
            root[main][sub][sub_sub] = {}

    def convert(d):
        return {k: convert(v) if isinstance(v, defaultdict) else v for k, v in d.items()}

    return convert(root)