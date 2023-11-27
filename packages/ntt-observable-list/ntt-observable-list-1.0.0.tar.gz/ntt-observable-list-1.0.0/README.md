# ntt-observable-list
ObservableList python

## Example

```python
from ntt_observable_list import ObservableList

def PrintList(lst: list) -> None:
    print(lst)

lst = ObservableList([3, 1, 4])
lst.Connect(PrintList)

lst.append(5)   # ---> [3, 1, 4, 5]
lst[1] = 3      # ---> [3, 3, 4, 5]
```