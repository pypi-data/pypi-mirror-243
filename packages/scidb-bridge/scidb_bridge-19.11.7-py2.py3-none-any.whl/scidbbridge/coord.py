import numpy
import pandas


def get_chunk_length(dims, chunk_coords, i):
    if dims[i].high_value != '*':
        return min(dims[i].chunk_length,
                   dims[i].high_value - chunk_coords[i] + 1)
    return dims[i].chunk_length


def coord2delta(data, dims, chunk_coords):
    n_dims = len(dims)

    if n_dims == 1:
        res = data[dims[0].name] - chunk_coords[0]
    elif n_dims == 2:
        res = ((data[dims[0].name] - chunk_coords[0])
               * get_chunk_length(dims, chunk_coords, 1)
               + data[dims[1].name] - chunk_coords[1])
    else:
        res = pandas.Series(numpy.zeros(len(data)), dtype=numpy.int64)
        for i in range(n_dims):
            res *= get_chunk_length(dims, chunk_coords, i)
            res += data[dims[i].name] - chunk_coords[i]

    df = pandas.DataFrame(res)
    df.columns = ('pos', )
    delta = df['pos'] - df.shift(1, fill_value=-1)['pos']
    return delta.to_list()


def delta2coord(data, schema, chunk_coords):
    d = data.copy(deep=False)   # Shallow copy to input DataFrame

    # Convert delta values to position values
    d['@pos'] = d['@delta']
    d.at[0, '@pos'] -= 1
    d['@pos'] = d['@pos'].cumsum()

    # Convert position values to coordinates
    dims = schema.dims
    n_dims = len(dims)
    for i in range(n_dims - 1, -1, -1):
        if i == 0:
            d[dims[i].name] = d['@pos'] + chunk_coords[i]
        else:
            d[dims[i].name] = (d['@pos'] % dims[i].chunk_length +
                               chunk_coords[i])
            d['@pos'] = d['@pos'] // dims[i].chunk_length

    return d[[a.name for a in schema.atts] +
             [d.name for d in dims]]


# util/ArrayCoordinatesMapper.h
#
# /**
#  * Convert array coordinates to the logical chunk position (in row-major
#  * order)
#  */
# position_t coord2pos(CoordinateCRange coord) const
# {
#     assert(coord.size() == _nDims);
#     position_t pos(-1);
#     if (_nDims == 1) {
#         pos = coord[0] - _origin[0];
#         assert(pos < _chunkIntervals[0]);
#     } else if (_nDims == 2) {
#         pos = (coord[0] - _origin[0])*_chunkIntervals[1] +
#             (coord[1] - _origin[1]);
#     } else {
#         pos = 0;
#         for (size_t i = 0, n = _nDims; i < n; i++) {
#             pos *= _chunkIntervals[i];
#             pos += coord[i] - _origin[i];
#         }
#     }
#     assert(pos >= 0 && static_cast<uint64_t>(pos)<_logicalChunkSize);
#     return pos;
# }
#
# /**
#  * Convert logical chunk position (in row-major order)  to array coordinates
#  */
# void pos2coord(position_t pos,CoordinateRange coord) const
# {
#     assert(pos >= 0);
#     assert(coord.size() == _nDims);
#     if (_nDims == 1) {
#         coord[0] = _origin[0] + pos;
#         assert(pos < _chunkIntervals[0]);
#     } else if (_nDims == 2) {
#         coord[1] = _origin[1] + (pos % _chunkIntervals[1]);
#         pos /= _chunkIntervals[1];
#         coord[0] = _origin[0] + pos;
#         assert(pos < _chunkIntervals[0]);
#     } else {
#         for (int i=safe_static_cast<int>(_nDims); --i>=0;) {
#             coord[i] = _origin[i] + (pos % _chunkIntervals[i]);
#             pos /= _chunkIntervals[i];
#         }
#         assert(pos == 0);
#     }
# }
