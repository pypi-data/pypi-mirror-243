
/** Copyright 2020 Alibaba Group Holding Limited.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

#ifndef GRAPE_GRAPH_ID_INDEXER_H_
#define GRAPE_GRAPH_ID_INDEXER_H_

#include <cmath>
#include <vector>

#include "flat_hash_map/flat_hash_map.hpp"
#include "grape/config.h"
#include "grape/types.h"
#include "grape/utils/string_view_vector.h"

namespace grape {

namespace id_indexer_impl {

static constexpr int8_t min_lookups = 4;
static constexpr double max_load_factor = 0.5f;

inline int8_t log2(size_t value) {
  static constexpr int8_t table[64] = {
      63, 0,  58, 1,  59, 47, 53, 2,  60, 39, 48, 27, 54, 33, 42, 3,
      61, 51, 37, 40, 49, 18, 28, 20, 55, 30, 34, 11, 43, 14, 22, 4,
      62, 57, 46, 52, 38, 26, 32, 41, 50, 36, 17, 19, 29, 10, 13, 21,
      56, 45, 25, 31, 35, 16, 9,  12, 44, 24, 15, 8,  23, 7,  6,  5};
  value |= value >> 1;
  value |= value >> 2;
  value |= value >> 4;
  value |= value >> 8;
  value |= value >> 16;
  value |= value >> 32;
  return table[((value - (value >> 1)) * 0x07EDD5E59A4E28C2) >> 58];
}

template <typename T>
struct KeyBuffer {
  using type = std::vector<T, Allocator<T>>;

  template <typename IOADAPTOR_T>
  static void serialize(std::unique_ptr<IOADAPTOR_T>& writer, type& buffer) {
    size_t size = buffer.size();
    CHECK(writer->Write(&size, sizeof(size_t)));
    if (size > 0) {
      CHECK(writer->Write(buffer.data(), size * sizeof(T)));
    }
  }

  template <typename IOADAPTOR_T>
  static void deserialize(std::unique_ptr<IOADAPTOR_T>& reader, type& buffer) {
    size_t size;
    CHECK(reader->Read(&size, sizeof(size_t)));
    if (size > 0) {
      buffer.resize(size);
      CHECK(reader->Read(buffer.data(), size * sizeof(T)));
    }
  }

  static void SendTo(const type& buffer, int dst_worker_id, int tag,
                     MPI_Comm comm) {
    sync_comm::Send(buffer, dst_worker_id, tag, comm);
  }

  static void RecvFrom(type& buffer, int src_worker_id, int tag,
                       MPI_Comm comm) {
    sync_comm::Recv(buffer, src_worker_id, tag, comm);
  }
};

template <>
struct KeyBuffer<nonstd::string_view> {
  using type = StringViewVector;

  template <typename IOADAPTOR_T>
  static void serialize(std::unique_ptr<IOADAPTOR_T>& writer, type& buffer) {
    size_t content_buffer_size = buffer.content_buffer().size();
    CHECK(writer->Write(&content_buffer_size, sizeof(size_t)));
    if (content_buffer_size > 0) {
      CHECK(writer->Write(buffer.content_buffer().data(),
                          content_buffer_size * sizeof(char)));
    }
    size_t offset_buffer_size = buffer.offset_buffer().size();
    CHECK(writer->Write(&offset_buffer_size, sizeof(size_t)));
    if (offset_buffer_size > 0) {
      CHECK(writer->Write(buffer.offset_buffer().data(),
                          offset_buffer_size * sizeof(size_t)));
    }
  }

  template <typename IOADAPTOR_T>
  static void deserialize(std::unique_ptr<IOADAPTOR_T>& reader, type& buffer) {
    size_t content_buffer_size;
    CHECK(reader->Read(&content_buffer_size, sizeof(size_t)));
    if (content_buffer_size > 0) {
      buffer.content_buffer().resize(content_buffer_size);
      CHECK(reader->Read(buffer.content_buffer().data(),
                         content_buffer_size * sizeof(char)));
    }
    size_t offset_buffer_size;
    CHECK(reader->Read(&offset_buffer_size, sizeof(size_t)));
    if (offset_buffer_size > 0) {
      buffer.offset_buffer().resize(offset_buffer_size);
      CHECK(reader->Read(buffer.offset_buffer().data(),
                         offset_buffer_size * sizeof(size_t)));
    }
  }

  static void SendTo(const type& buffer, int dst_worker_id, int tag,
                     MPI_Comm comm) {
    sync_comm::Send(buffer, dst_worker_id, tag, comm);
  }

  static void RecvFrom(type& buffer, int src_worker_id, int tag,
                       MPI_Comm comm) {
    sync_comm::Recv(buffer, src_worker_id, tag, comm);
  }
};

}  // namespace id_indexer_impl

template <typename KEY_T, typename INDEX_T>
class IdIndexer {
 public:
  using key_buffer_t = typename id_indexer_impl::KeyBuffer<KEY_T>::type;
  using ind_buffer_t = std::vector<INDEX_T, Allocator<INDEX_T>>;
  using dist_buffer_t = std::vector<int8_t, Allocator<int8_t>>;

  IdIndexer() : hasher_() { reset_to_empty_state(); }
  ~IdIndexer() {}

  size_t entry_num() const { return distances_.size(); }

  bool add(const KEY_T& oid, INDEX_T& lid) {
    size_t index =
        hash_policy_.index_for_hash(hasher_(oid), num_slots_minus_one_);

    int8_t distance_from_desired = 0;
    for (; distances_[index] >= distance_from_desired;
         ++index, ++distance_from_desired) {
      INDEX_T cur_lid = indices_[index];
      if (keys_[cur_lid] == oid) {
        lid = cur_lid;
        return false;
      }
    }

    lid = static_cast<INDEX_T>(keys_.size());
    keys_.push_back(oid);
    assert(keys_.size() == num_elements_ + 1);
    emplace_new_value(distance_from_desired, index, lid);
    assert(keys_.size() == num_elements_);
    return true;
  }

  bool add(KEY_T&& oid, INDEX_T& lid) {
    size_t index =
        hash_policy_.index_for_hash(hasher_(oid), num_slots_minus_one_);

    int8_t distance_from_desired = 0;
    for (; distances_[index] >= distance_from_desired;
         ++index, ++distance_from_desired) {
      INDEX_T cur_lid = indices_[index];
      if (keys_[cur_lid] == oid) {
        lid = cur_lid;
        return false;
      }
    }

    lid = static_cast<INDEX_T>(keys_.size());
    keys_.push_back(std::move(oid));
    assert(keys_.size() == num_elements_ + 1);
    emplace_new_value(distance_from_desired, index, lid);
    assert(keys_.size() == num_elements_);
    return true;
  }

  bool _add(const KEY_T& oid, size_t hash_value, INDEX_T& lid) {
    size_t index =
        hash_policy_.index_for_hash(hash_value, num_slots_minus_one_);

    int8_t distance_from_desired = 0;
    for (; distances_[index] >= distance_from_desired;
         ++index, ++distance_from_desired) {
      INDEX_T cur_lid = indices_[index];
      if (keys_[cur_lid] == oid) {
        lid = cur_lid;
        return false;
      }
    }

    lid = static_cast<INDEX_T>(keys_.size());
    keys_.push_back(oid);
    assert(keys_.size() == num_elements_ + 1);
    emplace_new_value(distance_from_desired, index, lid);
    assert(keys_.size() == num_elements_);
    return true;
  }

  bool _add(KEY_T&& oid, size_t hash_value, INDEX_T& lid) {
    size_t index =
        hash_policy_.index_for_hash(hash_value, num_slots_minus_one_);

    int8_t distance_from_desired = 0;
    for (; distances_[index] >= distance_from_desired;
         ++index, ++distance_from_desired) {
      INDEX_T cur_lid = indices_[index];
      if (keys_[cur_lid] == oid) {
        lid = cur_lid;
        return false;
      }
    }

    lid = static_cast<INDEX_T>(keys_.size());
    keys_.push_back(std::move(oid));
    assert(keys_.size() == num_elements_ + 1);
    emplace_new_value(distance_from_desired, index, lid);
    assert(keys_.size() == num_elements_);
    return true;
  }

  void _add(const KEY_T& oid) {
    size_t index =
        hash_policy_.index_for_hash(hasher_(oid), num_slots_minus_one_);

    int8_t distance_from_desired = 0;
    for (; distances_[index] >= distance_from_desired;
         ++index, ++distance_from_desired) {
      if (keys_[indices_[index]] == oid) {
        return;
      }
    }

    INDEX_T lid = static_cast<INDEX_T>(keys_.size());
    keys_.push_back(oid);
    assert(keys_.size() == num_elements_ + 1);
    emplace_new_value(distance_from_desired, index, lid);
    assert(keys_.size() == num_elements_);
  }

  void _add(KEY_T&& oid) {
    size_t index =
        hash_policy_.index_for_hash(hasher_(oid), num_slots_minus_one_);

    int8_t distance_from_desired = 0;
    for (; distances_[index] >= distance_from_desired;
         ++index, ++distance_from_desired) {
      if (keys_[indices_[index]] == oid) {
        return;
      }
    }

    INDEX_T lid = static_cast<INDEX_T>(keys_.size());
    keys_.push_back(std::move(oid));
    assert(keys_.size() == num_elements_ + 1);
    emplace_new_value(distance_from_desired, index, lid);
    assert(keys_.size() == num_elements_);
  }

  size_t bucket_count() const {
    return num_slots_minus_one_ ? num_slots_minus_one_ + 1 : 0;
  }

  bool empty() const { return (num_elements_ == 0); }

  size_t size() const { return num_elements_; }

  bool get_key(INDEX_T lid, KEY_T& oid) const {
    if (lid >= num_elements_) {
      return false;
    }
    oid = keys_[lid];
    return true;
  }

  bool get_index(const KEY_T& oid, INDEX_T& lid) const {
    size_t index =
        hash_policy_.index_for_hash(hasher_(oid), num_slots_minus_one_);
    for (int8_t distance = 0; distances_[index] >= distance;
         ++distance, ++index) {
      INDEX_T ret = indices_[index];
      if (keys_[ret] == oid) {
        lid = ret;
        return true;
      }
    }
    return false;
  }

  bool _get_index(const KEY_T& oid, size_t hash, INDEX_T& lid) const {
    size_t index = hash_policy_.index_for_hash(hash, num_slots_minus_one_);
    for (int8_t distance = 0; distances_[index] >= distance;
         ++distance, ++index) {
      INDEX_T ret = indices_[index];
      if (keys_[ret] == oid) {
        lid = ret;
        return true;
      }
    }
    return false;
  }

  void swap(IdIndexer<KEY_T, INDEX_T>& rhs) {
    keys_.swap(rhs.keys_);
    indices_.swap(rhs.indices_);
    distances_.swap(rhs.distances_);

    hash_policy_.swap(rhs.hash_policy_);
    std::swap(max_lookups_, rhs.max_lookups_);
    std::swap(num_elements_, rhs.num_elements_);
    std::swap(num_slots_minus_one_, rhs.num_slots_minus_one_);

    std::swap(hasher_, rhs.hasher_);
  }

  const key_buffer_t& keys() const { return keys_; }

  key_buffer_t& keys() { return keys_; }

  template <typename IOADAPTOR_T>
  void Serialize(std::unique_ptr<IOADAPTOR_T>& writer) {
    id_indexer_impl::KeyBuffer<KEY_T>::serialize(writer, keys_);
    InArchive arc;
    arc << hash_policy_.get_mod_function_index() << max_lookups_
        << num_elements_ << num_slots_minus_one_ << indices_.size()
        << distances_.size();
    CHECK(writer->WriteArchive(arc));
    arc.Clear();

    if (indices_.size() > 0) {
      CHECK(writer->Write(indices_.data(), indices_.size() * sizeof(INDEX_T)));
    }
    if (distances_.size() > 0) {
      CHECK(
          writer->Write(distances_.data(), distances_.size() * sizeof(int8_t)));
    }
  }

  template <typename IOADAPTOR_T>
  void Deserialize(std::unique_ptr<IOADAPTOR_T>& reader) {
    id_indexer_impl::KeyBuffer<KEY_T>::deserialize(reader, keys_);
    OutArchive arc;
    CHECK(reader->ReadArchive(arc));
    size_t mod_function_index;
    size_t indices_size, distances_size;
    arc >> mod_function_index >> max_lookups_ >> num_elements_ >>
        num_slots_minus_one_ >> indices_size >> distances_size;
    arc.Clear();

    hash_policy_.set_mod_function_by_index(mod_function_index);
    indices_.resize(indices_size);
    distances_.resize(distances_size);
    if (indices_size > 0) {
      CHECK(reader->Read(indices_.data(), indices_.size() * sizeof(INDEX_T)));
    }
    if (distances_size > 0) {
      CHECK(
          reader->Read(distances_.data(), distances_.size() * sizeof(int8_t)));
    }
  }

 private:
  void emplace(INDEX_T lid) {
    KEY_T key = keys_[lid];
    size_t index =
        hash_policy_.index_for_hash(hasher_(key), num_slots_minus_one_);
    int8_t distance_from_desired = 0;
    for (; distances_[index] >= distance_from_desired;
         ++index, ++distance_from_desired) {
      if (indices_[index] == lid) {
        return;
      }
    }

    emplace_new_value(distance_from_desired, index, lid);
  }

  void emplace_new_value(int8_t distance_from_desired, size_t index,
                         INDEX_T lid) {
    if (num_slots_minus_one_ == 0 || distance_from_desired == max_lookups_ ||
        num_elements_ + 1 >
            (num_slots_minus_one_ + 1) * id_indexer_impl::max_load_factor) {
      grow();
      return;
    } else if (distances_[index] < 0) {
      indices_[index] = lid;
      distances_[index] = distance_from_desired;
      ++num_elements_;
      return;
    }
    INDEX_T to_insert = lid;
    std::swap(distance_from_desired, distances_[index]);
    std::swap(to_insert, indices_[index]);
    for (++distance_from_desired, ++index;; ++index) {
      if (distances_[index] < 0) {
        indices_[index] = to_insert;
        distances_[index] = distance_from_desired;
        ++num_elements_;
        return;
      } else if (distances_[index] < distance_from_desired) {
        std::swap(distance_from_desired, distances_[index]);
        std::swap(to_insert, indices_[index]);
        ++distance_from_desired;
      } else {
        ++distance_from_desired;
        if (distance_from_desired == max_lookups_) {
          grow();
          return;
        }
      }
    }
  }

  void grow() { rehash(std::max(size_t(4), 2 * bucket_count())); }

  void rehash(size_t num_buckets) {
    num_buckets = std::max(
        num_buckets, static_cast<size_t>(std::ceil(
                         num_elements_ / id_indexer_impl::max_load_factor)));

    if (num_buckets == 0) {
      reset_to_empty_state();
      return;
    }

    auto new_prime_index = hash_policy_.next_size_over(num_buckets);
    if (num_buckets == bucket_count()) {
      return;
    }

    int8_t new_max_lookups = compute_max_lookups(num_buckets);

    dist_buffer_t new_distances(num_buckets + new_max_lookups);
    ind_buffer_t new_indices(num_buckets + new_max_lookups);

    size_t special_end_index = num_buckets + new_max_lookups - 1;
    for (size_t i = 0; i != special_end_index; ++i) {
      new_distances[i] = -1;
    }
    new_distances[special_end_index] = 0;

    new_indices.swap(indices_);
    new_distances.swap(distances_);

    std::swap(num_slots_minus_one_, num_buckets);
    --num_slots_minus_one_;
    hash_policy_.commit(new_prime_index);

    max_lookups_ = new_max_lookups;

    num_elements_ = 0;
    INDEX_T elem_num = static_cast<INDEX_T>(keys_.size());
    for (INDEX_T lid = 0; lid < elem_num; ++lid) {
      emplace(lid);
    }
  }

  void reset_to_empty_state() {
    keys_.clear();

    indices_.clear();
    distances_.clear();
    indices_.resize(id_indexer_impl::min_lookups);
    distances_.resize(id_indexer_impl::min_lookups, -1);
    distances_[id_indexer_impl::min_lookups - 1] = 0;

    num_slots_minus_one_ = 0;
    hash_policy_.reset();
    max_lookups_ = id_indexer_impl::min_lookups - 1;
    num_elements_ = 0;
  }

  static int8_t compute_max_lookups(size_t num_buckets) {
    int8_t desired = id_indexer_impl::log2(num_buckets);
    return std::max(id_indexer_impl::min_lookups, desired);
  }

  template <typename _T, typename _Enable>
  friend struct sync_comm::CommImpl;

  key_buffer_t keys_;
  ind_buffer_t indices_;
  dist_buffer_t distances_;

  ska::ska::prime_number_hash_policy hash_policy_;
  int8_t max_lookups_ = id_indexer_impl::min_lookups - 1;
  size_t num_elements_ = 0;
  size_t num_slots_minus_one_ = 0;

  std::hash<KEY_T> hasher_;
};

namespace sync_comm {

template <typename OID_T, typename VID_T>
struct CommImpl<IdIndexer<OID_T, VID_T>> {
  static void send(const IdIndexer<OID_T, VID_T>& indexer, int dst_worker_id,
                   int tag, MPI_Comm comm) {
    InArchive arc;
    arc << indexer.hash_policy_.get_mod_function_index() << indexer.max_lookups_
        << indexer.num_elements_ << indexer.num_slots_minus_one_;
    Send(arc, dst_worker_id, tag, comm);
    id_indexer_impl::KeyBuffer<OID_T>::SendTo(indexer.keys_, dst_worker_id, tag,
                                              comm);
    Send(indexer.indices_, dst_worker_id, tag, comm);
    Send(indexer.distances_, dst_worker_id, tag, comm);
  }

  static void recv(IdIndexer<OID_T, VID_T>& indexer, int src_worker_id, int tag,
                   MPI_Comm comm) {
    OutArchive arc;
    Recv(arc, src_worker_id, tag, comm);
    size_t mod_function_index;
    arc >> mod_function_index >> indexer.max_lookups_ >>
        indexer.num_elements_ >> indexer.num_slots_minus_one_;
    indexer.hash_policy_.set_mod_function_by_index(mod_function_index);
    id_indexer_impl::KeyBuffer<OID_T>::RecvFrom(indexer.keys_, src_worker_id,
                                                tag, comm);
    Recv(indexer.indices_, src_worker_id, tag, comm);
    Recv(indexer.distances_, src_worker_id, tag, comm);
  }
};

}  // namespace sync_comm

}  // namespace grape

#endif  // GRAPE_GRAPH_ID_INDEXER_H_
