
def build_category_tree(flat_categories):
    tree = {}
    for cat in flat_categories:
        main = cat['main_category']
        sub = cat['sub_category']
        sub_sub = cat.get('sub_sub_category', '')

        tree.setdefault(main, {})
        tree[main].setdefault(sub, {})

        if sub_sub:
            tree[main][sub][sub_sub] = {}

    return tree
