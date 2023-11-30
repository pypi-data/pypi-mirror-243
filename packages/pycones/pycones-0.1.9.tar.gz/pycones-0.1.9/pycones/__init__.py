"""
The pycones package provides useful functions
"""
import json
import math
import numpy as np

__version__ = "0.1.9"


def flatten(lst):
    """
    flatten a list
    """
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def list_join(*args, sep=""):
    """
    join lists into a string
    """
    res = sep.join(flatten(args))
    return res


def nb_kernel_switch(notebook_path, out_path, kernel="python"):
    """
    switch jupyter kernel into python or r
    """
    assert notebook_path.endswith(".ipynb"), "please input a .ipynb file"
    kernel = kernel.lower()
    assert kernel in ["python", "r"], "please switch to python or r kernel"

    notebook = json.loads(open(notebook_path, "r").read())
    if kernel == "r":
        notebook["metadata"]["kernelspec"]["name"] = "ir"
        notebook["metadata"]["kernelspec"]["display_name"] = "R"
        notebook["metadata"]["kernelspec"]["language"] = "R"
        notebook["metadata"]["language_info"] = {
            "codemirror_mode": "r",
            "file_extension": ".r",
            "mimetype": "text/x-r-source",
            "name": "R",
            "pygments_lexer": "r",
        }
    elif kernel == "python":
        notebook["metadata"]["kernelspec"]["name"] = "python3"
        notebook["metadata"]["kernelspec"]["display_name"] = \
                "Python 3 (ipykernel)"
        notebook["metadata"]["kernelspec"]["language"] = "python"
        notebook["metadata"]["language_info"] = {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
        }

    with open(out_path, "w") as f:
        json.dump(notebook, f)


def dfs_to_dicts(df_list, key_list):
    """
    trans dataframes which have same rownames and colnames into dicts
    """
    # same length check
    assert len(df_list) == len(key_list)

    # same colnames and rownames check
    for i in range(1, len(df_list)):
        assert all(df_list[i].columns == df_list[0].columns)
        assert all(df_list[i].index == df_list[0].index)

    res = dict()
    for colname, row in df_list[0].to_dict().items():
        res[colname] = dict()
        for rowname, value in row.items():
            res[colname][rowname] = dict()
            for i, res_key in enumerate(key_list):
                res[colname][rowname][res_key] = df_list[i].loc[rowname, colname]
    return res


def signif_number(x: float, digits: int = 2):
    """
    round a number to significant digits
    """
    # return None, np.nan
    if not x or np.isnan(x):
        return x
    
    x = float(x)
    digits = int(digits)
    digits = -int(math.floor(math.log10(abs(x)))) + (digits - 1)

    return round(x, digits)
