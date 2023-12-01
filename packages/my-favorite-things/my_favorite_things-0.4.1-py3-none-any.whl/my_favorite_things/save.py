"""
Contains method `save` with the flexibility of saving any number of object in various
ways to a specific directory and with other functions.
"""
import pickle
from pathlib import Path

import numpy as np


def save(
    name: str,
    savedir: str = "",
    savepath: str = "",
    stype: str = "npz",
    absolute: bool = False,
    parents: int = 0,
    overwrite: bool = False,
    append: bool = True,
    dryrun: bool = False,
    save_kwargs: dict = {},
    **files: ...,
) -> None:
    """
    Saves data to a file. If saving numpy arrays, use `stype="npz"`, to save as a .npz
    file. For other objects such as dicts, use `stype="pkl"` to pickle it.

    We start with: Path / `savepath` where Path is the CWD (either absolute or relative)
    and then we go up that path `parents` number of times. E.g. if we have
    savepath=one/two/three and parents=2 -- we are in Path/one. Next we tack on
    `savedir` and save to `name`. So if parents=0, then we save the file to
    Path / `savepath` / `savedir` / `name`. Otherwise, `parents` refers to the parent
    directories of `savepath`.

    Parameters:
    name - String representing name of file.
    savepath (default "") - Absolute or relative path to save file in depending on
        value of `absolute`.
    savedir (default "") - Directory to save in. Can be a path. This is added on top of
        `savepath` and after `parents` is applied.  So `parents` moves up the tree and
        `savedir` can move down a different branch.
    stype (default "npz") - File type, can be either "npz" or "npy" for saving numpy
        array(s) or "pkl" for saving anything as a pickle file.
    absolute (default False) - If True, we start in the directory `savepath`, move up it
        `parents` number of times, then append `savedir` to it. If False, we start in
        the directory $CWD/`savepath` and do the same thing.
    parents (default 0) - Which parent directory to save in. If 0, saves in same
        directory as this file. If 1, saves in parent directory. If 2, saves in
        grandparent directory. And so on.
    overwrite (default False) - If a file with the same path and file name exists,
        overwrite it if `overwrite=True`. Otherwise, (if append=True) append `_1` to the
        end of the file. If that is already taken, then append `_2` instead. And so on,
        until a unique number is found.
    append (default True) - If True and overwrite=False, append an int to the file name
        as described above in `overwrite` description. If False, abort. If
        overwrite=True, this keyword does nothing.
    dryrun (default False) - If True, will not save anything but only print out where
        the save will be to.
    save_kwargs (default {}) - Keyword arguments to pass to the function that is doing
        the savings, i.e. np.save, np.savez or pickle.dump. The method np.savez has no
        extra kwargs, so this is NOT passed to savez.
    files - Kwargs for the python objects to save.
    """
    if not absolute:
        # Relative path
        path = Path.cwd() / savepath
    else:
        # Absolute path
        path = Path() / savepath

    # Create path for where to save data
    if parents > 0:
        try:
            path = path.parents[parents - 1]
        except IndexError:
            raise IndexError(
                f"There is no {'grand' * parents}parent (parents={parents})"
                + f" folder for {path}"
            ) from None
    elif parents != 0:
        raise ValueError(
            f"`parents` must equal a nonnegative int but it is: parents={parents}."
        ) from None
    path = path / savedir
    path.mkdir(parents=True, exist_ok=True)

    file_exist = (path / (name + f".{stype}")).is_file()
    # If file already exist, save with appending number on the end, if append=True
    if file_exist and (not overwrite and append):
        ind = 1
        while True:
            if (path / (name + f"_{ind}.{stype}")).is_file():
                ind += 1
            else:
                name += f"_{ind}"
                break
        print(
            f"Saving with appended integer, {ind}, since file already exists. Delete "
            + "file or set `overwrite=True` to save without integer."
        )
    elif file_exist and (not overwrite and not append):
        # Otherwise don't save at all
        print(
            "File of the same name already exists. Delete file, set `overwrite=True` "
            + "or `append=True`. Aborting..."
        )
        return

    dr_txt = " This is a dryrun!" if dryrun else ""
    print(f"Saving to {path / (name + f'.{stype}')}.{dr_txt}")
    if dryrun:
        return

    # Save as the appropriate type
    match stype:
        case "npz":
            np.savez(path / name, **files)
        case "npy":
            if len(files.values()) != 1:
                raise IndexError(
                    f"Choosing stype={stype} allowing only a single array to be saved "
                    + f"but there are {len(files.values())} arrays passed as the"
                    + "`files` kwargs."
                ) from None
            np.save(path / name, arr=list(files.values())[0], **save_kwargs)
        case "pkl":
            with open(f"{path / name}.pkl", "wb") as savefile:
                pickle.dump(files, savefile, **save_kwargs)
