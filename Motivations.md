* [Motivations](#motivations)
    * [The Problem with Python](#the-problem-with-python) a case study
    * [Dynamic Python Julia interface](#dynamic-python-julia-interface)
    * [Caveats](#caveats)

## Motivations

I judge it highly probable that Julia provides a uniquely high-productivity environment for developing high-performance
Qiskit features. By high-productivity, I mean higher than Python. By high-performance, I mean
competitive with C or Rust. I base the judgment both on the nature of Julia and of Qiskit. In particular,
Qiskit is built around a large number of complicated pure-Python types, rather than thin wrappers around
standard numerical code. In the following, I present a selection of individual pieces of evidence to back up the judgment,
omitting some of the most important because they require a longer discussion.
However, the overall argument is inevitably rather polemical. The only way to test the judgment is through
experiments, such as this package.

* Julia is developed largely by applied mathematicians. It is dedicated to correct, performant, technical, computing.
But the developers are committed to providing a complete ecosystem, as expected of any ambitious modern language.
A successful full-stack [web framework](https://github.com/GenieFramework/Genie.jl)
is written in Julia.

* Julia is a dynamic language. It is as well suited as Python, I would argue better suited, for rapidly
exploring ideas. This project shows that experimenting with writing Qiskit functionality in Julia,
and exposing it via a Python package, can be done quickly and fruitfully.

* Idiomatic, straightforward, Julia code executes as fast as statically compiled languages.
In addition Julia offers many opportunities for further optimization without leaving the language;
For instance, using macros such as `@inbounds`, `@simd`, `@avx`, `@threads`, and specialized data
types.

* Native data structures are the same or similar to those in languages such as C++ and Rust.
    * Ideas developed in Julia may be ported to these languages and vice-versa. For instance, to
     Qiskit modules written in C++ or Rust.
    * Interfaces between Julia and these languages are straightforward and highly efficient.

* Julia is fully committed to a single, coherent, type system in all aspects of the language.

### The Problem with Python

A case study

* A large amount of Qiskit development effort is expended working around the fact that Python lacks the
features above. An example is the following sequence (and several issues linked within). The issue
involved trying to write both efficient and generic code in a hot location.
    * [Using a numpy integer type as an index for a QuantumRegister fails #3929](https://github.com/Qiskit/qiskit-terra/issues/3929)
    16 comments
    * [Allow numbers.Integral instead of only built-in int for QuantumRegister index #4591](https://github.com/Qiskit/qiskit-terra/pull/4591)
    25 comments, 25 commits.
    * [Performance regression in circuit construction because of type checking #4791](https://github.com/Qiskit/qiskit-terra/issues/4791)
    3 comments
    * [Fixed #4791: Explicity checked for several int types #4810](https://github.com/Qiskit/qiskit-terra/pull/4810)
    1 comment

    The solution was to enumerate possible types and take a small performance hit. Presumably, if further numpy derivatives
    need to be supported, we could weigh the benefit of supporting them vs the cost of adding more checks to the list.
    In contrast, in Julia,
    * Regarding different types of integers, `Int64`, `Int32`, etc.; one would, idiomatically, with little consideration,
      use a parametric type, possibly constrained by the supertype `Integer`.
    * Standard Julia arrays and all kinds of exotic arrays use the same set of integer types, so the issue of supporting
      different numerical packages, GPUs, AD, etc. in this context would not arise.
    * because of compilation and inlining, the check would take, rather than microseconds, strictly no time; it would be elided.
    * So, compared to the Python solution, the code would be far more generic, take far less engineering effort (none), and be
    far more efficient.

    I see similar issues arise over and over in Qiskit development. The productivity gain in developing Qiskit algorithms
    in Julia rather than Python would be, by my rough, not-quite-semi-quantitative, estimate, about ten times. I mean
    medium scale development. Larger than the Jordan-Wigner implementation below, but less than reproducing all of Qiskit.
    It would be interesting, but very difficult, to try to support this estimate with evidence. I think a better approach
    is to carry out experiments such as qiskit_alt.

### Dynamic Python Julia interface

* There are a few good options for using Python and Julia together. The approach here uses
pyjulia, which offers the Python module `julia`. This allows mixing Julia and Python modules
dynamically and rapidly with no interface code required. Conversions of data types is handled
by pyjulia. You can call existing Julia modules or define them from Python. For example,
```python
In [1]  from julia import Main
In [2]: Main.eval("""
    ...: module Foo
    ...:     calc(array, num) = array .+ num
    ...: end""");
In [3]: Main.Foo.calc([1, 2, 3], 4)
Out[3]: array([5, 6, 7], dtype=int64)
```
Here, we have defined a function `calc` in a  Julia module `Foo`.
The input Python list is converted to a Julia array. And the returned Julia array is converted to
a numpy array. Here is an example of how we convert a user defined type from Julia to Python.
```python
def jlPauliList(pauli_list):
    """
    Convert a QiskitQuantumInfo.PauliList to a qiskit.quantum_info.PauliList
    """
    return PauliList.from_symplectic(pauli_list.z, pauli_list.x)
```

### Caveats

* Julia is neither purely interpreted nor traditionally statically compiled. What it "is" evolves;
just-ahead-of-time compiled is a useful description.
But, it doesn't have all the advantages of a language that is largely committed to one (Python) or the other (Rust) model.
In the past, the JIT (or JAOT) penalty was typically large and there weren't a lot of good ways to mitigate it.
The situation today is much, much, improved on several fronts. But, it is still an issue.
At the moment
    * The JIT penalty for qiskit_alt is not great (for someone who started using Julia in 2015).
    First, about 8 seconds to import `qiskit_alt`. Then there are various delays
    for compiling code paths. There are large Julia dependencies that might be attractive, but that incur larger JIT penalties. One
    would have to weigh the consequences of adopting them.
    * But, the penalty is not static, rather it is improving. Ongoing developments include switching to the interpreter;
    more fine-grained optimization and code specialization levels; techniques to avoid cache-invalidations in the method table,
    a huge source of compilation cost.
    * One can reduce the start-up penalty by loading on demand. The [current system](https://github.com/JuliaPackaging/Requires.jl)
    is ok, but a bit ad-hoc and limited. There is talk about improving it, which should require only ordinary engineering effort.
    In fact, we use it to get around a hard dependency on `pyscf`, but I will likely make `pyscf` a hard dependency.
    * One can make a fully AOT-compiled system image. Currently, we can build this locally in `qiskit_alt` in less than five minutes.
    The basic tooling is there, and improving, but could be more polished.
    We are rolling-our own functions and scripts. How robust it is, is a crucial
    question. During development, currently, you *cannot* use the system image. The compiled-in package cannot be replaced dynamically.
    For development, we instead rely on [Revise](./Development.md).

* Julia is not magic, performance-pixie-dust. This should go without saying, but the misconception is encountered frequently enough to
be dangerous to projects. I have seen a relatively small amount of not-to-obscure numba code easily outperform a Julia package.
Using Julia effectively requires learning
some [basic guidelines](https://docs.julialang.org/en/v1/manual/performance-tips/). They are not really difficult to learn and
to employ, but are not optional. So, a good Julia project requires a certain amount of Julia culture. Is it more than that required
for a quality Python project? I think likely not, but it is an important question.

* Julia does not (yet) have multiple inheritance. More generally, understanding how to best use multiple dispatch, traits, various macro-based embellishments
to the type system is perhaps not as mature as the understanding of design in Python.
However, some of the [most ancient (9 years old), large packages](https://github.com/JuliaStats/Distributions.jl)
have weathered the changes relatively well and are still widely used.

* The key creator of Julia, Jeff Bezanson, can tell you [What's bad about Julia](https://www.youtube.com/watch?v=TPuJsgyu87U) in 2019.
This covers the points above and many others.
