# RoverRetriever: A Python Wrapper for the Dog CEO API

RoverRetriever is a lightweight Python wrapper written to facilitate interaction with [Dog CEO's API](https://dog.ceo/dog-api/).

## Usage

### Initialize the client

```python
from RoverRetriever.retriever import Retriever
dog_api = Retriever()
```

### Get a list of breeds

```python
breeds = dog_api.get_breeds()
```

### Get a random dog image

```python
random_image = dog_api.get_random_image()
```

### Get images by breed

```python
images = dog_api.get_images_by_breed('bulldog')
```

### Get all sub-breeds

```python
sub_breeds = dog_api.get_all_sub_breeds('bulldog')
```