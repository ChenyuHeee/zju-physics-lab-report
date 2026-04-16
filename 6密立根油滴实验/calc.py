import math

eta = 1.81e-5; g = 9.793; rho_oil = 981.0; rho_air = 1.205
drho = rho_oil - rho_air; b0 = 8.226e-3; p = 101800; d = 5e-3; e_ref = 1.602e-19
b0_2p = b0 / (2 * p)

data = [
    (1,171,1.5e-3,[22.15,21.91,22.48,21.92,21.52]),
    (2,150,1.5e-3,[29.24,29.08,29.60,29.15,29.32]),
    (3,166,0.5e-3,[12.05,11.43,11.59,11.52,11.49]),
    (4,185,0.25e-3,[6.10,5.47,6.20,5.65,5.81]),
    (5,185,0.25e-3,[3.71,3.73,4.21,4.10,4.20]),
    (6,105,0.25e-3,[1.15,1.11,1.22,1.00,1.01]),
    (7,122,0.25e-3,[5.90,6.23,5.40,5.72,5.48]),
    (8,122,0.25e-3,[10.59,10.92,9.46,9.24,9.56]),
    (9,106,0.25e-3,[8.97,8.71,9.20,8.53,8.25]),
    (10,93,0.25e-3,[10.52,9.41,10.56,11.52,9.98]),
]

results = []
for (i,U,L,times) in data:
    t_bar = sum(times)/5
    vg = L/t_bar
    r = math.sqrt(9*eta*vg/(2*g*drho))
    r_p = -b0_2p + math.sqrt(b0_2p**2 + r**2)
    m = (4/3)*math.pi*r_p**3*drho
    q = m*g*d/U
    n = round(q/e_ref)
    n = max(n,1)
    ei = q/n
    results.append({'i':i,'vg':vg,'r_p':r_p,'m':m,'q':q,'n':n,'ei':ei})
    print(f"{i:2d}  vg={vg*1e3:.5f}  r'={r_p*1e6:.4f}  m={m*1e16:.4f}  q={q*1e19:.4f}  n={n}  ei={ei*1e19:.4f}")

valid = [r for r in results if r['n']<10]
ei_vals = [r['ei'] for r in valid]
N = len(ei_vals)
e_bar = sum(ei_vals)/N
uA = math.sqrt(sum((e-e_bar)**2 for e in ei_vals)/(N*(N-1)))
delta = abs(e_bar-e_ref)/e_ref*100
print(f"\nN={N}, ebar={e_bar*1e19:.4f}, uA={uA*1e19:.4f}, delta={delta:.2f}%")
