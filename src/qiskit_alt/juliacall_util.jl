function pyconvert_list(::Type{T}, list) where T
    vec = Vector{T}(undef, length(list))
    for i in eachindex(list)
        vec[i] = PythonCall.pyconvert(T, list[i])
    end
    return vec
end

const pytype_str = PythonCall.pytype(PythonCall.Py("c"))
const pytype_int = PythonCall.pytype(PythonCall.Py(1))
const pytype_float = PythonCall.pytype(PythonCall.Py(1.0))

function pyconvert_list(pT::PythonCall.Py, list)
    if isequal(pytype_str, pT)
        T = String
    elseif isequal(pytype_int, pT)
        T = Int
    elseif isequal(pytype_float, pT)
        T = Float64
    else
        println("Unsupported")
        return nothing  # should throw an error
    end
    return pyconvert_list(T, list)
end
