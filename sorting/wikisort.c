#include <Python.h>

/* Function prototypes */
static void reverse_range(int *array, int start, int end);
static void rotate(int *array, int start, int mid, int end);
static int binary_search_left(int *array, int value, int start, int end);
static void merge(int *array, int start, int mid, int end);
static void merge_sort(int *array, int start, int end);

/* Python callable function */
static PyObject *wikisort(PyObject *self, PyObject *args)
{
    PyObject *array_obj;
    Py_ssize_t n;

    /* Parse arguments */
    if (!PyArg_ParseTuple(args, "O", &array_obj))
    {
        return NULL;
    }

    /* Check that array_obj is a list */
    if (!PyList_Check(array_obj))
    {
        PyErr_SetString(PyExc_TypeError, "Expected a list");
        return NULL;
    }

    /* Get array length */
    n = PyList_Size(array_obj);
    if (n == -1)
    {
        return NULL;
    }

    /* Convert Python list to C array */
    int *array = (int *)malloc(n * sizeof(int));
    if (array == NULL)
    {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        return NULL;
    }

    for (Py_ssize_t i = 0; i < n; ++i)
    {
        PyObject *item = PyList_GetItem(array_obj, i);
        if (!PyLong_Check(item))
        {
            free(array);
            PyErr_SetString(PyExc_TypeError, "List must contain integers");
            return NULL;
        }
        array[i] = PyLong_AsLong(item);
    }

    /* Perform WikiSort */
    merge_sort(array, 0, n);

    /* Convert C array back to Python list */
    for (Py_ssize_t i = 0; i < n; ++i)
    {
        PyObject *item = PyLong_AsLong(array[i]);
        PyList_SetItem(array_obj, i, item);
    }

    free(array);

    /* Return sorted list */
    Py_INCREF(array_obj);
    return array_obj;
}

/* Helper functions */
static void reverse_range(int *array, int start, int end)
{
    while (start < end)
    {
        int tmp = array[start];
        array[start] = array[end];
        array[end] = tmp;
        start++;
        end--;
    }
}

static void rotate(int *array, int start, int mid, int end)
{
    reverse_range(array, start, mid - 1);
    reverse_range(array, mid, end - 1);
    reverse_range(array, start, end - 1);
}

static int binary_search_left(int *array, int value, int start, int end)
{
    while (start < end)
    {
        int mid = (start + end) / 2;
        if (array[mid] < value)
        {
            start = mid + 1;
        }
        else
        {
            end = mid;
        }
    }
    return start;
}

static void merge(int *array, int start, int mid, int end)
{
    int left_length = mid - start;
    int *left = (int *)malloc(left_length * sizeof(int));
    if (left == NULL)
    {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        return;
    }

    /* Copy left part to temporary array */
    for (int i = 0; i < left_length; ++i)
    {
        left[i] = array[start + i];
    }

    int left_index = 0;
    int right_index = mid;
    int k = start;

    while (left_index < left_length && right_index < end)
    {
        if (left[left_index] <= array[right_index])
        {
            array[k++] = left[left_index++];
        }
        else
        {
            array[k++] = array[right_index++];
        }
    }

    while (left_index < left_length)
    {
        array[k++] = left[left_index++];
    }

    free(left);
}

static void merge_sort(int *array, int start, int end)
{
    if (end - start < 2)
    {
        return;
    }

    int mid = (start + end) / 2;
    merge_sort(array, start, mid);
    merge_sort(array, mid, end);
    merge(array, start, mid, end);
}

/* Module method table */
static PyMethodDef WikiSortMethods[] = {
    {"wikisort", wikisort, METH_VARARGS, "Sorts a list using WikiSort algorithm."},
    {NULL, NULL, 0, NULL}};

/* Module initialization function */
static struct PyModuleDef wikisortmodule = {
    PyModuleDef_HEAD_INIT,
    "wikisort",
    NULL,
    -1,
    WikiSortMethods};

/* Module initialization */
PyMODINIT_FUNC PyInit_wikisort(void)
{
    return PyModule_Create(&wikisortmodule);
}