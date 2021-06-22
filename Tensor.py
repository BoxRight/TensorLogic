

def get_sesma_product(m1, atoms1, m2, atoms2):
  #Create tensors
  if not m1 or not m2:
    return []
  t2 = torch.tensor(m2, device=device)
  t1 = torch.tensor(m1, device=device)
  am1 = torch.tensor([atoms1], device = device)
  am2 = torch.tensor([atoms2], device = device)
  am1 = torch.cat([am1]*t1.shape[0], 0)
  am2 = torch.cat([am2]*t2.shape[0], 0)
  #Flatten the tensors
  t1_f = torch.flatten(t1)
  t2_f = torch.flatten(t2)
  am1_f = torch.flatten(am1)
  am2_f = torch.flatten(am2)
  t1.shape
  am1.shape
  #First product
  c = t1_f[:,None].eq(t2_f)
  m = am1_f[:,None].eq(am2_f)
  c = m*c
  c = c.long()
  return c

def add_plausibility(table):
  t1 = torch.tensor(table, device=device)
  t2 = torch.tensor(table, device=device)
  t1 = torch.unsqueeze(t1, 0)
  t2 = torch.unsqueeze(t2, 0)
  t2 = torch.cat((t1, t2), 0)
  t2 = t2.tolist()
  return t2

def get_negation(m1, atoms1):
  a = tuple(itertools.product([0, 1], repeat=len(atoms1)))
  m1 = set(tuple(elem) for elem in m1)
  a = set(a)
  a = a.difference(m1)
  a = list(list(elem) for elem in a)
  return [atoms1, a]

def create_all_possibilities(atoms1):
  a = tuple(itertools.product([0, 1], repeat=len(atoms1)))
  a = list(list(elem) for elem in a)
  return [atoms1, a]

def get_intersection(m1, atoms1, m2, atoms2):
  if len(m2) >= len(m1):
    c = get_sesma_product(m1, atoms1, m2, atoms2)
    a = m1
    aa = atoms1
    b = m2
    ba = atoms2
  else:
    c = get_sesma_product(m2, atoms2, m1, atoms1)
    a = m2
    aa = atoms2
    b = m1
    ba = atoms1
  if c == [] and not c:
    atoms_intersection = list(dict.fromkeys(aa + ba))
    return [atoms_intersection, []]
  elif not c.tolist():
    atoms_intersection = list(dict.fromkeys(aa + ba))
    return [atoms_intersection, []]
  j = 0
  k = 0
  l = len(a[0])
  m = len(b[0])
  minimum_truth = len(list(set(aa).intersection(ba)))
  quadrants = len(a) * len(b)
  intersection = []
  atoms_intersection = list(dict.fromkeys(aa + ba))
  #Creates products quadrants
  for i in range(quadrants):
    if j > len(c[0]) - m:
      j = 0
      k = k + l
    d = torch.narrow(c, 1, j, m)
    d = torch.narrow(d, 0, k, l)
    #saca los valores de verdad de la interseccion
    if d.count_nonzero() == minimum_truth:
      dicto = {}
      for atom in range(len(aa)):
        dicto[aa[atom]] = a[int(k/l)][atom] 
      for atom in range(len(ba)):
        dicto[ba[atom]] = b[int(j/m)][atom]
      hola = []
      for variable in atoms_intersection:
          hola.append(dicto[variable])
      intersection.append(hola)
    j = j + m

  return [atoms_intersection, intersection]

def get_intersection_3D(m1, atoms1, m2, atoms2):
  intersection = []
  for i in range(len(m1)):
    uno = get_intersection(m1[i], atoms1, m2, atoms2)
    intersection.append(uno[1])
    if i == len(m1) - 1:
      intersection = [uno[0]] + [intersection]
  return intersection

def get_negation_3D(m1, atoms1, m2, atoms2):
  negation = get_negation(m2, atoms2)
  intersection = get_intersection_3D(m1, atoms1, negation[1], negation[0])
  return intersection

def get_implication(m1, atoms1, m2, atoms2):
  NotQ = get_negation(m2, atoms2)
  pAndNotQ = get_intersection(m1, atoms1, NotQ[1], NotQ[0])
  pImpliesQ = get_negation(pAndNotQ[1], pAndNotQ[0])
  return pImpliesQ

def get_equivalence(m1, atoms1, m2, atoms2):
  pImpliesQ = get_implication(m1, atoms1, m2, atoms2)
  qImpliesP = get_implication(m2, atoms2, m1, atoms1)
  pIffQ = get_intersection(pImpliesQ[1], pImpliesQ[0], qImpliesP[1], qImpliesP[0])
  return pIffQ

def get_union(m1, atoms1, m2, atoms2):
  NotQ = get_negation(m2, atoms2)
  NotP = get_negation(m1, atoms1)
  NotPAndNotQ = get_intersection(NotQ[1], NotQ[0], NotP[1], NotP[0])
  pOrQ = get_negation(NotPAndNotQ[1], NotPAndNotQ[0])
  return pOrQ

def operational_diamond(m1, atoms1, m2, atoms2):
  t1 = torch.tensor(m1, device=device)
  t2 = torch.tensor([], device=device)
  for i in atoms2:
    index = atoms1.index(i)
    column = t1[:, index:index+1]
    t2 = torch.cat((t2, column), 1)
  t2 = torch.unique(t2, dim=0)
  t2 = t2.long()
  t2 = t2.tolist()
  m2 = set(tuple(elem) for elem in m2)
  t2 = set(tuple(elem) for elem in t2)
  if m2.issubset(t2):
    a = tuple(itertools.product([0, 1], repeat=len(atoms1)))
    a = list(list(elem) for elem in a)
    return [atoms1, a]
  else:
    b = get_negation(m1, atoms1)
    return [atoms1, b[1]]
  
  def operational_box(m1, atoms1, m2, atoms2):
    not_p = get_negation(m2, atoms2)
    diamond_not_p = operational_diamond(m1, atoms1, not_p[1], not_p[0])
    diamond_not_p = get_intersection(diamond_not_p[1], diamond_not_p[0], not_p[1], not_p[0])
    box_p = get_negation(diamond_not_p[1], diamond_not_p[0])
    box_p = get_intersection(m1, atoms1, box_p[1], box_p[0])
    return box_p 
  
def diamond_in(m1, atoms1, m2, atoms2, plausibility):
  m = m1[plausibility - 1]
  diamond_p = operational_diamond(m, atoms1, m2, atoms2)
  check = get_intersection(diamond_p[1], diamond_p[0], m, atoms1)
  check = set(tuple(elem) for elem in check[1])
  m = set(tuple(elem) for elem in m)
  if m == check:
    return [atoms1, m1]
  else:
    return [atoms1, []]
  
def box_in(m1, atoms1, m2, atoms2, plausibility):
  m = m1[plausibility - 1]
  box_p = operational_box(m, atoms1, m2, atoms2)
  m1[plausibility-1] = box_p[1]
  return m1
