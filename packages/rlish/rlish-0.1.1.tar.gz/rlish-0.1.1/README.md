# rlish

Saving and loading information in Python should be shorter and easier

<img src="img/art.png" width="300" title="hover text">
  

`rlish` is a Python package for simple and efficient data serialization and deserialization. It supports both `pickle` and `joblib` serialization methods, making it suitable for a wide range of data types, including large NumPy arrays and machine learning models.

## Installation

You can install `rlish` using pip:

```bash
pip install rlish
```

## Usage

### Saving Data

To save data, use the `save` function. You can choose between `pickle` and `joblib` formats:

```python
import rlish

data = {'a': 1, 'b': 2, 'c': 3}
filename = 'mydata'

# Save data using pickle
rlish.save(data, filename)

# Save data using joblib
rlish.save(data, 'mydata.joblib', format='joblib')
```

### Loading Data

To load data, use the `load` function:

```python
# Load data saved with pickle
loaded_data_pickle = rlish.load(filename)

# Load data saved with joblib
loaded_data_joblib = rlish.load('mydata.joblib')
```

## Contributing

Contributions to `rlish` are welcome! Feel free to open an issue or submit a pull request.
