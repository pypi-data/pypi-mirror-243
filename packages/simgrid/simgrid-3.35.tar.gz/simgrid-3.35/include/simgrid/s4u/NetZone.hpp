/* Copyright (c) 2016-2023. The SimGrid Team. All rights reserved.               */

/* This program is free software; you can redistribute it and/or modify it
 * under the terms of the license (GNU LGPL) which comes with this package. */

#ifndef SIMGRID_S4U_NETZONE_HPP
#define SIMGRID_S4U_NETZONE_HPP

#include "simgrid/s4u/Host.hpp"
#include <simgrid/forward.h>
#include <simgrid/s4u/Link.hpp>
#include <xbt/graph.h>
#include <xbt/signal.hpp>

#include <map>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

namespace simgrid::s4u {

/** @brief Networking Zones
 *
 * A netzone is a network container, in charge of routing information between elements (hosts) and to the nearby
 * netzones. In SimGrid, there is a hierarchy of netzones, with a unique root zone (that you can retrieve from the
 * s4u::Engine).
 */
class XBT_PUBLIC NetZone {
#ifndef DOXYGEN
  friend kernel::routing::NetZoneImpl;
#endif

  kernel::routing::NetZoneImpl* const pimpl_;

protected:
  explicit NetZone(kernel::routing::NetZoneImpl* impl) : pimpl_(impl) {}

public:
  /** @brief Retrieves the name of that netzone as a C++ string */
  const std::string& get_name() const;
  /** @brief Retrieves the name of that netzone as a C string */
  const char* get_cname() const;

  NetZone* get_parent() const;
  NetZone* set_parent(const NetZone* parent);
  std::vector<NetZone*> get_children() const;

  std::vector<Host*> get_all_hosts() const;
  size_t get_host_count() const;

  kernel::routing::NetZoneImpl* get_impl() const { return pimpl_; }

  /** Get the properties assigned to a netzone */
  const std::unordered_map<std::string, std::string>* get_properties() const;
  /** Retrieve the property value (or nullptr if not set) */
  const char* get_property(const std::string& key) const;
  void set_property(const std::string& key, const std::string& value);
  /** @brief Get the netpoint associated to this netzone */
  kernel::routing::NetPoint* get_netpoint() const;
  /** @brief Get the gateway associated to this netzone */
  kernel::routing::NetPoint* get_gateway() const;
  kernel::routing::NetPoint* get_gateway(const std::string& name) const;
  void set_gateway(const s4u::Host* router) { set_gateway(router->get_netpoint()); }
  void set_gateway(kernel::routing::NetPoint* router);
  void set_gateway(const std::string& name, kernel::routing::NetPoint* router);

  void extract_xbt_graph(const s_xbt_graph_t* graph, std::map<std::string, xbt_node_t, std::less<>>* nodes,
                         std::map<std::string, xbt_edge_t, std::less<>>* edges);

  /* Add content to the netzone, at parsing time. It should be sealed afterward. */
  unsigned long add_component(kernel::routing::NetPoint* elm); /* A host, a router or a netzone, whatever */

  /**
   * @brief Add a route between 2 netzones, and same in other direction
   * @param src Source netzone
   * @param dst Destination netzone
   * @param links List of links
   */
  void add_route(const NetZone* src, const NetZone* dst, const std::vector<const Link*>& links);

/**
   * @brief Add a route between 2 netzones, and same in other direction
   * @param src Source netzone
   * @param dst Destination netzone
   * @param link_list List of links and their direction used in this communication
   * @param symmetrical Bi-directional communication
   */
  void add_route(const NetZone* src, const NetZone* dst, const std::vector<LinkInRoute>& link_list, bool symmetrical = true);

#ifndef DOXYGEN
  /**
   * @brief Add a route between 2 netpoints
   *
   * Create a route:
   * - route between 2 hosts/routers in same netzone, no gateway is needed
   * - route between 2 netzones, connecting 2 gateways.
   *
   * @param src Source netzone's netpoint
   * @param dst Destination netzone' netpoint
   * @param gw_src Netpoint of the gateway in the source netzone
   * @param gw_dst Netpoint of the gateway in the destination netzone
   * @param link_list List of links and their direction used in this communication
   * @param symmetrical Bi-directional communication
   */
  //(we should first remove the Python binding in v3.35) XBT_ATTRIB_DEPRECATED_v339("Please call add_route either from
  // Host to Host or NetZone to NetZone")
  void add_route(kernel::routing::NetPoint* src, kernel::routing::NetPoint* dst, kernel::routing::NetPoint* gw_src,
                 kernel::routing::NetPoint* gw_dst, const std::vector<LinkInRoute>& link_list, bool symmetrical = true);
  /**
   * @brief Add a route between 2 netpoints, and same in other direction
   *
   * Create a route:
   * - route between 2 hosts/routers in same netzone, no gateway is needed
   * - route between 2 netzones, connecting 2 gateways.
   *
   * @param src Source netzone's netpoint
   * @param dst Destination netzone' netpoint
   * @param gw_src Netpoint of the gateway in the source netzone
   * @param gw_dst Netpoint of the gateway in the destination netzone
   * @param link_list List of links
   */
  XBT_ATTRIB_DEPRECATED_v339("Please call add_route either from Host to Host or NetZone to NetZone") void add_route(
      kernel::routing::NetPoint* src, kernel::routing::NetPoint* dst, kernel::routing::NetPoint* gw_src,
      kernel::routing::NetPoint* gw_dst, const std::vector<const Link*>& links);
#endif

  /**
   * @brief Add a route between 2 hosts
   *
   * @param src Source host
   * @param dst Destination host
   * @param link_list List of links and their direction used in this communication
   * @param symmetrical Bi-directional communication
   */
  void add_route(const Host* src, const Host* dst, const std::vector<LinkInRoute>& link_list, bool symmetrical = true);
  /**
   * @brief Add a route between 2 hosts
   *
   * @param src Source host
   * @param dst Destination host
   * @param links List of links. The UP direction will be used on src->dst and DOWN direction on dst->src
   */
  void add_route(const Host* src, const Host* dst, const std::vector<const Link*>& links);

  void add_bypass_route(kernel::routing::NetPoint* src, kernel::routing::NetPoint* dst,
                        kernel::routing::NetPoint* gw_src, kernel::routing::NetPoint* gw_dst,
                        const std::vector<LinkInRoute>& link_list);

private:
#ifndef DOXYGEN
  static xbt::signal<void(NetZone const&)> on_creation;
  static xbt::signal<void(NetZone const&)> on_seal;
#endif

public:
  /** \static Add a callback fired on each newly created NetZone */
  static void on_creation_cb(const std::function<void(NetZone const&)>& cb) { on_creation.connect(cb); }
  /** \static Add a callback fired on each newly sealed NetZone */
  static void on_seal_cb(const std::function<void(NetZone const&)>& cb) { on_seal.connect(cb); }

  /**
   * @brief Create a host
   *
   * @param name Host name
   * @param speed_per_pstate Vector of CPU's speeds
   */
  s4u::Host* create_host(const std::string& name, const std::vector<double>& speed_per_pstate);
  s4u::Host* create_host(const std::string& name, double speed);
  /**
   * @brief Create a Host (string version)
   *
   * @throw std::invalid_argument if speed format is incorrect.
   */
  s4u::Host* create_host(const std::string& name, const std::vector<std::string>& speed_per_pstate);
  s4u::Host* create_host(const std::string& name, const std::string& speed);

  /**
   * @brief Create a link
   *
   * @param name Link name
   * @param bandwidths Link's speed (vector for wifi links)
   * @throw std::invalid_argument if bandwidth format is incorrect.
   */
  s4u::Link* create_link(const std::string& name, const std::vector<double>& bandwidths);
  s4u::Link* create_link(const std::string& name, double bandwidth);

  /** @brief Create a link (string version) */
  s4u::Link* create_link(const std::string& name, const std::vector<std::string>& bandwidths);
  s4u::Link* create_link(const std::string& name, const std::string& bandwidth);

  /**
   * @brief Create a split-duplex link
   *
   * In SimGrid, split-duplex links are a composition of 2 regular (shared) links (up/down).
   *
   * This function eases its utilization by creating the 2 links for you. We append a suffix
   * "_UP" and "_DOWN" to your link name to identify each of them.
   *
   * Both up/down links have exactly the same bandwidth
   *
   * @param name Name of the link
   * @param bandwidth Speed
   */
  s4u::SplitDuplexLink* create_split_duplex_link(const std::string& name, const std::string& bandwidth);
  s4u::SplitDuplexLink* create_split_duplex_link(const std::string& name, double bandwidth);

  kernel::resource::NetworkModel* get_network_model() const;

  /**
   * @brief Make a router within that NetZone
   *
   * @param name Router name
   */
  kernel::routing::NetPoint* create_router(const std::string& name);

  /** @brief Seal this netzone configuration */
  NetZone* seal();

  void
  set_latency_factor_cb(std::function<double(double size, const s4u::Host* src, const s4u::Host* dst,
                                             const std::vector<s4u::Link*>& /*links*/,
                                             const std::unordered_set<s4u::NetZone*>& /*netzones*/)> const& cb) const;
  void
  set_bandwidth_factor_cb(std::function<double(double size, const s4u::Host* src, const s4u::Host* dst,
                                               const std::vector<s4u::Link*>& /*links*/,
                                               const std::unordered_set<s4u::NetZone*>& /*netzones*/)> const& cb) const;
};

// External constructors so that the types (and the types of their content) remain hidden
XBT_PUBLIC NetZone* create_full_zone(const std::string& name);
XBT_PUBLIC NetZone* create_star_zone(const std::string& name);
XBT_PUBLIC NetZone* create_dijkstra_zone(const std::string& name, bool cache);
XBT_PUBLIC NetZone* create_empty_zone(const std::string& name);
XBT_PUBLIC NetZone* create_floyd_zone(const std::string& name);
XBT_PUBLIC NetZone* create_vivaldi_zone(const std::string& name);
XBT_PUBLIC NetZone* create_wifi_zone(const std::string& name);

// Extra data structure for complex constructors

/** @brief Aggregates the callbacks used to build clusters netzones (Torus/Dragronfly/Fat-Tree) */
struct ClusterCallbacks {
  /**
   * @brief Callback used to set the netpoint and gateway located at some leaf of clusters (Torus, FatTree, etc)
   *
   * The netpoint can be either a host, router or another netzone.
   * Gateway must be non-null if netpoint is a netzone
   *
   * @param zone: The newly create zone, needed for creating new resources (hosts, links)
   * @param coord: the coordinates of the element
   * @param id: Internal identifier of the element
   * @return pair<NetPoint*, NetPoint*>: returns a pair of netpoint and gateway.
   */
  // XBT_ATTRIB_DEPRECATED_v339
  using ClusterNetPointCb = std::pair<kernel::routing::NetPoint*, kernel::routing::NetPoint*>(
      NetZone* zone, const std::vector<unsigned long>& coord, unsigned long id);

   /**
   * @brief Callback used to set the NetZone located at some leaf of clusters (Torus, FatTree, etc)
   *
   * @param zone: The parent zone, needed for creating new resources (hosts, links)
   * @param coord: the coordinates of the element
   * @param id: Internal identifier of the element
   * @return NetZone*: returns newly created netzone
   */
  using ClusterNetZoneCb = NetZone*(NetZone* zone, const std::vector<unsigned long>& coord, unsigned long id);
  /**
   * @brief Callback used to set the Host located at some leaf of clusters (Torus, FatTree, etc)
   *
   * @param zone: The parent zone, needed for creating new resources (hosts, links)
   * @param coord: the coordinates of the element
   * @param id: Internal identifier of the element
   * @return Host*: returns newly created host
   */
  using ClusterHostCb = Host*(NetZone* zone, const std::vector<unsigned long>& coord, unsigned long id);

  /**
   * @brief Callback used to set the links for some leaf of the cluster (Torus, FatTree, etc)
   *
   * The coord parameter depends on the cluster being created:
   * - Torus: Direct translation of the Torus' dimensions, e.g. (0, 0, 0) for a 3-D Torus
   * - Fat-Tree: A pair (level in the tree, id), e.g. (0, 0): first leaf and (1,0): first switch at level 1.
   * - Dragonfly: a tuple (group, chassis, blades/routers, nodes), e.g. (0, 0, 0, 0) for first node in the cluster.
   * Important: To identify the router inside a "group, chassis, blade", we use MAX_UINT in the last parameter (e.g. 0,
   * 0, 0, 4294967295).
   *
   * @param zone: The newly create zone, needed for creating new resources (hosts, links)
   * @param coord: the coordinates of the element
   * @param id: Internal identifier of the element
   * @return Pointer to the Link
   */
  using ClusterLinkCb = Link*(NetZone* zone, const std::vector<unsigned long>& coord, unsigned long id);

  bool by_netzone_ = false;
  bool is_by_netzone() const { return by_netzone_; }
  bool by_netpoint_ = false; // XBT_ATTRIB_DEPRECATED_v339
  bool is_by_netpoint() const { return by_netpoint_; } // XBT_ATTRIB_DEPRECATED_v339
  std::function<ClusterNetPointCb> netpoint; // XBT_ATTRIB_DEPRECATED_v339
  std::function<ClusterHostCb> host;
  std::function<ClusterNetZoneCb> netzone;
  std::function<ClusterLinkCb> loopback = {};
  std::function<ClusterLinkCb> limiter  = {};
  explicit ClusterCallbacks(const std::function<ClusterNetZoneCb>& set_netzone)
      : by_netzone_(true), netzone(set_netzone){/* nothing to do */};

  ClusterCallbacks(const std::function<ClusterNetZoneCb>& set_netzone,
                   const std::function<ClusterLinkCb>& set_loopback, const std::function<ClusterLinkCb>& set_limiter)
      :  by_netzone_(true), netzone(set_netzone), loopback(set_loopback), limiter(set_limiter){/* nothing to do */};

  explicit ClusterCallbacks(const std::function<ClusterHostCb>& set_host)
      : host(set_host) {/* nothing to do */};

  ClusterCallbacks(const std::function<ClusterHostCb>& set_host,
                   const std::function<ClusterLinkCb>& set_loopback, const std::function<ClusterLinkCb>& set_limiter)
      :  host(set_host), loopback(set_loopback), limiter(set_limiter){/* nothing to do */};

  XBT_ATTRIB_DEPRECATED_v339("Please use callback with either a Host/NetZone creation function as first parameter")
  explicit ClusterCallbacks(const std::function<ClusterNetPointCb>& set_netpoint)
      : by_netpoint_(true), netpoint(set_netpoint){/* nothing to do */};
  XBT_ATTRIB_DEPRECATED_v339("Please use callback with either a Host/NetZone creation function as first parameter")
  ClusterCallbacks(const std::function<ClusterNetPointCb>& set_netpoint,
                   const std::function<ClusterLinkCb>& set_loopback, const std::function<ClusterLinkCb>& set_limiter)
      : by_netpoint_(true), netpoint(set_netpoint), loopback(set_loopback), limiter(set_limiter){/* nothing to do */};
};
/**
 * @brief Create a torus zone
 *
 * Torus clusters are characterized by:
 * - dimensions, eg. {3,3,3} creates a torus with X = 3 elements, Y = 3 and Z = 3. In total, this cluster have 27
 * elements
 * - inter-node communication: (bandwidth, latency, sharing_policy) the elements are connected through regular links
 * with these characteristics
 * More details in: <a href="https://simgrid.org/doc/latest/Platform_examples.html?highlight=torus#torus-cluster">Torus
 * Cluster</a>
 *
 * Moreover, this method accepts 3 callbacks to populate the cluster: set_netpoint, set_loopback and set_limiter .
 *
 * Note that the all elements in a Torus cluster must have (or not) the same elements (loopback and limiter)
 *
 * @param name NetZone's name
 * @param parent Pointer to parent's netzone (nullptr if root netzone). Needed to be able to create the resources inside
 * the netzone
 * @param dimensions List of positive integers (> 0) which determines the torus' dimensions
 * @param set_callbacks Callbacks to set properties from cluster elements (netpoint, loopback and limiter)
 * @param bandwidth Characteristics of the inter-nodes link
 * @param latency Characteristics of the inter-nodes link
 * @param sharing_policy Characteristics of the inter-nodes link
 * @return Pointer to new netzone
 */
XBT_PUBLIC NetZone* create_torus_zone(const std::string& name, const NetZone* parent,
                                      const std::vector<unsigned long>& dimensions,
                                      const ClusterCallbacks& set_callbacks, double bandwidth, double latency,
                                      Link::SharingPolicy sharing_policy);

/** @brief Aggregates the parameters necessary to build a Fat-tree zone */
struct XBT_PUBLIC FatTreeParams {
  unsigned int levels;
  std::vector<unsigned int> down;
  std::vector<unsigned int> up;
  std::vector<unsigned int> number;
  FatTreeParams(unsigned int n_levels, const std::vector<unsigned int>& down_links,
                const std::vector<unsigned int>& up_links, const std::vector<unsigned int>& links_number);
};
/**
 * @brief Create a Fat-Tree zone
 *
 * Fat-Tree clusters are characterized by:
 * - levels: number of levels in the cluster, e.g. 2 (the final tree will have n+1 levels)
 * - downlinks: for each level, how many connections between elements below them, e.g. 2, 3: level 1 nodes are connected
 * to 2 nodes in level 2, which are connected to 3 nodes below. Determines the number total of leaves in the tree.
 * - uplinks: for each level, how nodes are connected, e.g. 1, 2
 * - link count: for each level, number of links connecting the nodes, e.g. 1, 1
 *
 * The best way to understand it is looking to the doc available in: <a
 * href="https://simgrid.org/doc/latest/Platform_examples.html#fat-tree-cluster">Fat Tree Cluster</a>
 *
 * Moreover, this method accepts 3 callbacks to populate the cluster: set_netpoint, set_loopback and set_limiter .
 *
 * Note that the all elements in a Fat-Tree cluster must have (or not) the same elements (loopback and limiter)
 *
 * @param name NetZone's name
 * @param parent Pointer to parent's netzone (nullptr if root netzone). Needed to be able to create the resources inside
 * the netzone
 * @param parameters Characteristics of this Fat-Tree
 * @param set_callbacks Callbacks to set properties from cluster elements (netpoint, loopback and limiter)
 * @param bandwidth Characteristics of the inter-nodes link
 * @param latency Characteristics of the inter-nodes link
 * @param sharing_policy Characteristics of the inter-nodes link
 * @return Pointer to new netzone
 */
XBT_PUBLIC NetZone* create_fatTree_zone(const std::string& name, const NetZone* parent, const FatTreeParams& parameters,
                                        const ClusterCallbacks& set_callbacks, double bandwidth, double latency,
                                        Link::SharingPolicy sharing_policy);

/** @brief Aggregates the parameters necessary to build a Dragonfly zone */
struct XBT_PUBLIC DragonflyParams {
  std::pair<unsigned int, unsigned int> groups;
  std::pair<unsigned int, unsigned int> chassis;
  std::pair<unsigned int, unsigned int> routers;
  unsigned int nodes;
  DragonflyParams(const std::pair<unsigned int, unsigned int>& groups,
                  const std::pair<unsigned int, unsigned int>& chassis,
                  const std::pair<unsigned int, unsigned int>& routers, unsigned int nodes);
};
/**
 * @brief Create a Dragonfly zone
 *
 * Dragonfly clusters are characterized by:
 * - groups: number of groups and links between each group, e.g. 2,2.
 * - chassis: number of chassis in each group and the number of links used to connect the chassis, e.g. 2,3
 * - routers: number of routers in each chassis and their links, e.g. 3,1
 * - nodes: number of nodes connected to each router using a single link, e.g. 2
 *
 * In total, the cluster will have groups * chassis * routers * nodes elements/leaves.
 *
 * The best way to understand it is looking to the doc available in: <a
 * href="https://simgrid.org/doc/latest/Platform_examples.html#dragonfly-cluster">Dragonfly Cluster</a>
 *
 * Moreover, this method accepts 3 callbacks to populate the cluster: set_netpoint, set_loopback and set_limiter .
 *
 * Note that the all elements in a Dragonfly cluster must have (or not) the same elements (loopback and limiter)
 *
 * @param name NetZone's name
 * @param parent Pointer to parent's netzone (nullptr if root netzone). Needed to be able to create the resources inside
 * the netzone
 * @param parameters Characteristics of this Dragonfly
 * @param set_callbacks Callbacks to set properties from cluster elements (netpoint, loopback and limiter)
 * @param bandwidth Characteristics of the inter-nodes link
 * @param latency Characteristics of the inter-nodes link
 * @param sharing_policy Characteristics of the inter-nodes link
 * @return Pointer to new netzone
 */
XBT_PUBLIC NetZone* create_dragonfly_zone(const std::string& name, const NetZone* parent,
                                          const DragonflyParams& parameters, const ClusterCallbacks& set_callbacks,
                                          double bandwidth, double latency, Link::SharingPolicy sharing_policy);

} // namespace simgrid::s4u

#endif /* SIMGRID_S4U_NETZONE_HPP */
