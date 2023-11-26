import pickle
import joblib

def save(data, filename, format='pickle'):
    """
    This function saves your data to a file. You can pick between 'pickle' and 'joblib' for saving.
    
    How it works:
        - Falls back on 'pickle' for everything else.
        - It also keeps a note (in a separate .meta file) of how your data was saved, so you don't have to remember.

    Parameters
    ----------------------
        data: (user-defined)
            The data you want to save as a file
        filename: string
            Where you want to save your data - just give me the file name.
        format: Choose 'pickle' or 'joblib' to save your data. 'pickle' is the default. Tip: Use 'joblib' if you're dealing with large arrays and/or machine learning models
    """
        # Save the data using the specified format
    if format == 'joblib':
        joblib.dump(data, filename)
    else:  # Default to pickle
        with open(filename, 'wb') as f:
            pickle.dump(data, f)

    # Store the format in a separate metadata file
    with open(filename + '.meta', 'w') as metafile:
        metafile.write(format)

def load(filename,format=None):
    """
    Need your data back? Just tell me the file name and I'll fetch it for you.
    
    This function remembers how your data was saved, so you don't need to worry about that.

    Returns:
        Your data, just as you saved it. No fuss, no muss.

    Parameters
    ----------------------
        filename: string
            The name of the file you want to load your data from.
        format : string
            Auxiliary input serialization format. "format" kwarg supercedes format read from .meta file if declared
    """
    # Read the format from the metadata file
    try:
        with open(filename + '.meta', 'r') as metafile:
            format_read = metafile.read().strip()
            format = format_read
    except FileNotFoundError:
        # raise FileNotFoundError("Metadata file not found. Cannot determine the serialization format.")
        None

    # Load the data using the determined format
    if format == 'joblib':
        return joblib.load(filename)
    else:
        with open(filename, 'rb') as f:
            return pickle.load(f)

