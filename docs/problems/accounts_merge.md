# [Accounts Merge](https://leetcode.com/problems/accounts-merge/)

**Medium** | **30 minutes** | **Graph**

**Pattern:** [Union-Find](../patterns/union_find/intuition.md)

**Practice:** [`practice/accounts_merge/solution.py`](../../practice/accounts_merge/solution.py)

Given a list of accounts where each element `accounts[i]` is a list of strings, where the first element `accounts[i][0]` is a name, and the rest of the elements are emails representing emails of the account.

Now, we would like to merge these accounts. Two accounts definitely belong to the same person if there is some common email to both accounts. Note that even if two accounts have the same name, they may belong to different people as people could have the same name. A person can have any number of accounts initially, but all of their accounts definitely have the same name.

After merging the accounts, return the accounts in the following format: the first element of each account is the name, and the rest of the elements are emails in sorted order. The accounts themselves can be returned in any order.

## Examples

### Example 1

**Input:**

```
accounts = [["John","johnsmith@mail.com","john_newyork@mail.com"],["John","johnsmith@mail.com","john00@mail.com"],["Mary","mary@mail.com"],["John","johnnybravo@mail.com"]]
```

**Output:**

```
[["John","john00@mail.com","john_newyork@mail.com","johnsmith@mail.com"],["Mary","mary@mail.com"],["John","johnnybravo@mail.com"]]
```

**Explanation:** The first and second John's are the same person as they have the common email "johnsmith@mail.com". The third John and Mary are different people as none of their emails are used by other accounts. We could return these lists in any order, for example the answer `[['Mary', 'mary@mail.com'], ['John', 'johnnybravo@mail.com'], ['John', 'john00@mail.com', 'john_newyork@mail.com', 'johnsmith@mail.com']]` would still be accepted.

### Example 2

**Input:**

```
accounts = [["Gabe","Gabe0@m.co","Gabe3@m.co","Gabe1@m.co"],["Kevin","Kevin3@m.co","Kevin5@m.co","Kevin0@m.co"],["Ethan","Ethan5@m.co","Ethan4@m.co","Ethan0@m.co"],["Hanzo","Hanzo3@m.co","Hanzo1@m.co","Hanzo0@m.co"],["Fern","Fern5@m.co","Fern1@m.co","Fern0@m.co"]]
```

**Output:**

```
[["Ethan","Ethan0@m.co","Ethan4@m.co","Ethan5@m.co"],["Gabe","Gabe0@m.co","Gabe1@m.co","Gabe3@m.co"],["Hanzo","Hanzo0@m.co","Hanzo1@m.co","Hanzo3@m.co"],["Kevin","Kevin0@m.co","Kevin3@m.co","Kevin5@m.co"],["Fern","Fern0@m.co","Fern1@m.co","Fern5@m.co"]]
```

## Constraints

- `1 <= accounts.length <= 1000`
- `2 <= accounts[i].length <= 10`
- `1 <= accounts[i][j].length <= 30`
- `accounts[i][0]` consists of English letters.
- `accounts[i][j]` (for `j > 0`) is a valid email.

## Solutions

### Brute Force

```python
class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        # Each entry: [name, set of emails]. Start with one group per account.
        groups = [[account[0], set(account[1:])] for account in accounts]

        # Repeatedly fuse any two groups that share an email, until a full
        # pass finds nothing to merge.
        merged_something = True
        while merged_something:
            merged_something = False
            i = 0
            while i < len(groups):
                j = i + 1
                while j < len(groups):
                    # Two groups belong to the same person if their email sets
                    # intersect at all.
                    if groups[i][1] & groups[j][1]:
                        groups[i][1] |= groups[j][1]
                        groups.pop(j)
                        merged_something = True
                    else:
                        j += 1
                i += 1

        # Emit each surviving group: name followed by its emails sorted.
        return [[name] + sorted(emails) for name, emails in groups]
```

#### Approach

Two accounts belong to the same person exactly when they share an email, so the
most direct idea is to keep merging overlapping accounts until none overlap. Each
account starts as its own group, and we fuse any two groups whose email sets
intersect, repeating until a full sweep changes nothing.

1. Turn each account into a `[name, set-of-emails]` group.
2. Compare every pair of groups. When two share at least one email, absorb the
   second group's emails into the first and remove the second.
3. Because a merge can create a new overlap with a group already checked, restart
   the sweeps and keep going until a complete pass merges nothing.
4. Emit each remaining group as its name followed by the emails in sorted order.

The repeated passes are what make this correct: merging a chain like `A-B` then
`B-C` requires revisiting groups, and looping until a clean pass guarantees every
transitive link is resolved.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(A^3 × K)`

Let `A` be the number of accounts and `K` the emails per account. Each pass
compares every pair of groups (`O(A^2)`) and each comparison intersects two email
sets (`O(K)`). In the worst case a pass merges only one pair, so up to `O(A)`
passes are needed, pushing the bound to `O(A^3 × K)` before sorting. This is
far heavier than the connectivity-based solutions.

##### Space Complexity: `O(N)`

The groups collectively hold every email once, where `N` is the total number of
emails, so auxiliary storage is linear.

#### Key Insights

- The merge rule reads directly off the problem statement: overlapping email sets
  mean the same person, so fuse and repeat.
- Looping until a pass changes nothing is what handles transitive chains, where
  merging one pair exposes a new overlap elsewhere.
- Set intersection (`&`) and union (`|=`) express "share an email" and "combine
  accounts" with no graph or disjoint-set machinery.
- Correct but slow: the repeated all-pairs sweeps are the obvious cost the graph
  and union-find approaches eliminate.

### DFS Connected Components

```python
from collections import defaultdict


class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        graph = defaultdict(set)  # email -> set of directly connected emails
        owner = {}                # email -> account name

        # Build an undirected graph: every email in an account links to the
        # account's first email, so all of them sit in one connected component.
        for account in accounts:
            name = account[0]
            first = account[1]
            for email in account[1:]:
                owner[email] = name
                graph[first].add(email)
                graph[email].add(first)

        visited = set()

        def dfs(start: str) -> list:
            # Iterative DFS collects every email reachable from start.
            stack = [start]
            component = []
            while stack:
                email = stack.pop()
                if email in visited:
                    continue
                visited.add(email)
                component.append(email)
                for neighbor in graph[email]:
                    if neighbor not in visited:
                        stack.append(neighbor)
            return component

        result = []
        for email in graph:
            if email not in visited:
                component = dfs(email)
                # Prefix the sorted emails with the shared account name.
                result.append([owner[email]] + sorted(component))
        return result
```

#### Approach

Two accounts belong to the same person exactly when they share an email. We can
model this directly as a graph where each email is a node and emails appearing
together in an account are connected by edges. Each connected component of that
graph is one merged person, and a depth-first search recovers every component.

1. For each account, add edges between the first email and every other email in
   that account. Because connectivity is transitive, linking each email to a
   single representative (the first) suffices to bind the whole account together,
   and chains across accounts merge through shared emails.
2. Record each email's owner name as it is registered.
3. Run a DFS from every unvisited email, collecting all reachable emails into one
   component.
4. For each component, emit the owner's name followed by the emails sorted
   alphabetically.

Building the adjacency graph from scratch keeps the logic explicit: the merge is
nothing more than enumerating connected components, and DFS is the most direct
way to walk them.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N × K + N log K)`

Let `N` be the total number of emails and `K` the size of the largest merged
account. Building the graph and running DFS visit each email and edge once. Edges
per account are bounded by its size, so traversal is `O(N × K)` in the worst case
where one giant component forms. Sorting each component totals `O(N log K)`. In
practice both terms are commonly summarized as `O(N log N)`.

##### Space Complexity: `O(N × K)`

The adjacency graph stores up to `O(K)` neighbors per email in the worst case,
the `owner` map and `visited` set are `O(N)`, and the DFS stack is bounded by the
component size.

#### Key Insights

- Treating emails as graph nodes makes the merge a textbook connected-components
  problem, no special data structure required beyond a dictionary of adjacency
  sets.
- Linking every email to the account's first email (a star within each account)
  is enough to connect the account; full pairwise edges are unnecessary.
- An iterative DFS with an explicit stack sidesteps any recursion-depth concern
  on a component that could span thousands of emails.
- The owner name comes from any email in the component, since one component maps
  to exactly one person.

### Union-Find

```python
from collections import defaultdict


class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        parent = {}          # email -> parent email (union-find forest)
        owner = {}           # email -> account name

        def find(email: str) -> str:
            # Path compression: flatten the chain toward the root.
            while parent[email] != email:
                parent[email] = parent[parent[email]]
                email = parent[email]
            return email

        def union(a: str, b: str) -> None:
            parent[find(a)] = find(b)

        # Register every email and union all emails that share an account.
        for account in accounts:
            name = account[0]
            first = account[1]
            for email in account[1:]:
                if email not in parent:
                    parent[email] = email
                    owner[email] = name
                union(email, first)

        # Group every email under the representative root of its component.
        groups = defaultdict(list)
        for email in parent:
            groups[find(email)].append(email)

        # Build each merged account: name followed by sorted emails.
        return [[owner[root]] + sorted(emails)
                for root, emails in groups.items()]
```

#### Approach

Two accounts belong to the same person exactly when they share an email, and
"shares an email" is a connectivity relation that is reflexive, symmetric, and
transitive. That makes union-find the natural fit: treat each email as a node,
connect all emails that appear together in one account, and each connected
component becomes one merged person.

1. For every account, register each email in the union-find forest (parent
   pointing to itself initially) and record its owner name.
2. Union every email in an account with the account's first email. After
   processing all accounts, emails reachable through any chain of shared accounts
   land in the same component.
3. Walk all emails and group them by their component root via `find`.
4. For each group, emit the owner's name followed by the emails in sorted order.

Using the email strings themselves as union-find keys avoids a separate
index-mapping step. Any email in a component can supply the name because all
accounts in one component share the same person and therefore the same name.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N × α(N) + N log K)`

Let `N` be the total number of emails across all accounts and `K` the size of
the largest merged account. The union-find operations cost `O(N × α(N))`, where
`α` is the inverse Ackermann function (effectively constant). Sorting the emails
within each group totals `O(N log K)` in the worst case, which dominates and is
commonly written simply as `O(N log N)`.

##### Space Complexity: `O(N)`

The `parent`, `owner`, and `groups` structures each hold one entry per distinct
email, so auxiliary space is linear in the number of emails.

#### Key Insights

- Modeling "shares an email" as a connectivity relation turns a fuzzy merge into
  a clean connected-components problem solvable with union-find.
- Using the email strings directly as forest keys removes the bookkeeping of
  mapping emails to integer ids.
- Unioning every email to the account's first email (rather than pairwise across
  all emails) is enough to connect the whole account, and it is simpler.
- Path compression keeps `find` near-constant, so even 1000 accounts with up to
  10 emails each resolve quickly.
- The owner name can be pulled from any email in a component, since a merged
  component always corresponds to a single person with one name.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(A^3 × K)` - Up to `O(A)` passes, each comparing all `O(A^2)` group pairs with an `O(K)` set intersection.
- **DFS Connected Components**: `O(N × K + N log K)` - Graph construction and traversal touch each email and edge once, then each component is sorted.
- **Union-Find**: `O(N × α(N) + N log K)` - Near-constant union/find operations per email, then per-component sorting; the inverse-Ackermann factor makes connectivity effectively faster than explicit traversal.

### Space Complexity

- **Brute Force**: `O(N)` - The groups collectively hold each email once.
- **DFS Connected Components**: `O(N × K)` - The adjacency graph can store up to `O(K)` neighbors per email when accounts are large.
- **Union-Find**: `O(N)` - Only flat parent and owner maps, one entry per email.

### Trade-offs

- **Brute Force**: Mirrors the problem statement directly (overlapping email sets merge), but the repeated all-pairs sweeps make it the slowest by far.
- **DFS Connected Components**: Builds the graph explicitly, which makes the connected-components structure obvious, but the adjacency sets cost more memory than a flat parent array.
- **Union-Find**: More compact in memory and asymptotically faster on the connectivity step, at the cost of the less-intuitive disjoint-set machinery.

### When to Use Each

- **Brute Force**: As a teaching baseline or for tiny inputs, where the merge-until-stable idea is easiest to reason about.
- **DFS Connected Components**: When clarity matters or when an explicit graph is already available, since the merge reads as a plain component walk.
- **Union-Find (Recommended)**: Best for interviews and large inputs - it is the most space-efficient and the standard answer for dynamic-connectivity merges.

### Optimization Notes

- The brute force re-scans every group pair on each pass; the graph and union-find approaches eliminate the quadratic re-checking by modeling connectivity once.
- The DFS approach trades extra adjacency-set memory for conceptual simplicity; switching the recursion to an explicit stack (as shown) keeps it safe on huge components.
- Union-find with path compression keeps the connectivity step near-linear, so for the largest inputs it edges out the explicit graph traversal.
- Both approaches are dominated by the per-component sort in practice, so neither can drop below `O(N log K)` while emails must be returned in sorted order.
- Linking each account's emails to a single representative (rather than all pairs) keeps edge count low in both solutions.
