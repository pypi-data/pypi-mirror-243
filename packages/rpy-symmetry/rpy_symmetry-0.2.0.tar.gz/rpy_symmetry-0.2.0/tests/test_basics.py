import unittest


def test_install_on_fly():
    import rpy_symmetry as rsym

    rsym.get_module('symmetry')


def test_minimal():
    import rpy_symmetry as rsym

    pval = rsym.p_symmetry([1, 2, 3])
    assert pval


def test_wo_cache():
    import rpy_symmetry as rsym

    assert rsym.rpy_symmetry._imported_package
    rsym.rpy_symmetry.ALLOW_CACHING = False
    rsym.rpy_symmetry._imported_package = {}
    pval = rsym.p_symmetry([1, 2, 3])

    assert pval
    assert rsym.rpy_symmetry._imported_package == {}


class RaiseMod(unittest.TestCase):
    def test_raises(self):
        import rpy_symmetry as rsym

        with self.assertRaises(ModuleNotFoundError):
            rsym.get_module('no_such_module')
