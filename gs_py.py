import json
import requests

ARQ_USUARIOS = "usuarios.json"

PROFISSOES = {
    "Desenvolvedor Backend": ["Lógica", "Python", "Git", "Banco De Dados", "Apis Rest"],
    "Desenvolvedor Frontend": ["Html", "Css", "Javascript", "Git", "React"],
    "Analista de Dados": ["Excel", "Python", "Sql", "Estatística", "Power Bi"],
    "Suporte Técnico": ["Hardware", "Redes", "Atendimento", "Sistemas Operacionais"],
    "Administrador de Sistemas": ["Linux", "Redes", "Segurança", "Docker", "Monitoramento"]
}

CURSOS = {
    "Lógica": "Curso em Vídeo - Lógica",
    "Python": "Curso em Vídeo - Python",
    "Git": "Udemy Git & GitHub (Gratuito)",
    "Banco de Dados": "Fundação Bradesco - Banco de Dados",
    "APIs REST": "Roadmap.sh - REST APIs",
    "HTML": "W3Schools - HTML",
    "CSS": "W3Schools - CSS",
    "JavaScript": "Curso em Vídeo - JavaScript",
    "React": "freeCodeCamp Frontend",
    "Excel": "Fundação Bradesco - Excel",
    "SQL": "Fundação Bradesco - SQL",
    "Estatística": "Khan Academy Estatística",
    "Power BI": "Microsoft Learn Power BI",
    "Hardware": "SENAI - Hardware Básico",
    "Redes": "SENAI Redes",
    "Atendimento": "Curso Gratuito Atendimento",
    "Sistemas Operacionais": "Apostilas - Introdução a SO",
    "Linux": "Linux Journey",
    "Segurança": "Cybrary Security Basics",
    "Docker": "Docker Docs",
    "Monitoramento": "Grafana/Prometheus (Artigos)"
}

def ler_usuarios():
    try:
        with open(ARQ_USUARIOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def salvar_usuarios(lista):
    with open(ARQ_USUARIOS, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False, indent=2)

def criar_conta(usuarios):
    print("\n=== Criar Conta ===")
    nome = input("Nome: ").strip()
    email = input("Email: ").strip().lower()
    senha = input("Senha: ")

    usuarios.append({
        "nome": nome,
        "email": email,
        "senha": senha,
        "profissoes": []
    })
    salvar_usuarios(usuarios)
    print("✅ Conta criada com sucesso!")

def login(usuarios):
    print("\n=== Login ===")
    email = input("Email: ").strip().lower()
    senha = input("Senha: ")
    for u in usuarios:
        if u["email"] == email and u["senha"] == senha:
            print(f"\n✅ Bem-vindo, {u['nome']}!")
            return u
    print("⚠️ Email ou senha incorretos.")
    return None

def frase_motivacional():
    try:
        r = requests.get("https://zenquotes.io/api/random", timeout=10)
        d = r.json()
        return f'"{d[0]["q"]}" — {d[0]["a"]}'
    except:
        return None

def escolher_profissao():
    print("\n=== Profissões Disponíveis ===")
    for i, p in enumerate(PROFISSOES.keys(), 1):
        print(f"{i}. {p}")

    try:
        index = int(input("Escolha: ")) - 1
        return list(PROFISSOES.keys())[index]
    except:
        print("⚠️ Opção inválida.")
        return None

def adicionar_profissao(user, usuarios):
    prof = escolher_profissao()
    if not prof:
        return

    exigidas = PROFISSOES[prof]
    print(f"\n📌 A profissão **{prof}** exige as seguintes habilidades:\n")
    for h in exigidas:
        print("-", h)

    habilidades_tidas = []
    print("\nDigite agora apenas as habilidades que você já possui.")
    while True:
        h = input("Habilidade (ou ENTER para parar): ").strip().title()
        if h == "":
            break
        habilidades_tidas.append(h)

    faltando = [h for h in exigidas if h not in habilidades_tidas]

    user["profissoes"].append({
        "nome": prof,
        "habilidades": habilidades_tidas,
        "faltando": faltando
    })

    salvar_usuarios(usuarios)

    print("\n✅ Profissão adicionada!")
    print("Você ainda precisa aprender:", ", ".join(faltando) if faltando else "Nada! 🎉")

    frase = frase_motivacional()
    if frase:
        print("\n💬 Motivação:", frase)

def selecionar_profissao_usuario(user):
    print("\n=== Suas Profissões ===")
    for i, p in enumerate(user["profissoes"], 1):
        print(f"{i}. {p['nome']}")
    try:
        index = int(input("Escolha: ")) - 1
        return user["profissoes"][index]
    except:
        print("⚠️ Opção inválida.")
        return None

def adicionar_habilidades(user, usuarios):
    prof = selecionar_profissao_usuario(user)
    if not prof:
        return

    print(f"\n=== Adicionar habilidades para {prof['nome']} ===")
    while True:
        h = input("Nova habilidade (ou ENTER para sair): ").strip().title()
        if h == "":
            break

        if h not in prof["habilidades"]:
            prof["habilidades"].append(h)

        if h in prof["faltando"]:
            prof["faltando"].remove(h)

    salvar_usuarios(usuarios)
    print("\n✅ Habilidades atualizadas!")

def ver_perfil(user):
    print("\n=== SEU PERFIL ===")
    print("Nome:", user["nome"])

    if not user["profissoes"]:
        print("Nenhuma profissão cadastrada ainda.")
        return

    for p in user["profissoes"]:
        print("\n📌", p["nome"])
        print("• Habilidades:", ", ".join(p["habilidades"]) if p["habilidades"] else "Nenhuma ainda")
        print("• Faltando:", ", ".join(p["faltando"]) if p["faltando"] else "Nada! Você está pronto 😎")

        if p["faltando"]:
            print("\n→ Recomendações de Cursos:")
            for h in p["faltando"]:
                curso = CURSOS.get(h, "Pesquisar no YouTube")
                print(f"{h}: {curso}")

def main():
    usuarios = ler_usuarios()
    user = None

    while True:
        if user is None:
            print("\n=== SISTEMA FUTURO DO TRABALHO ===")
            print("1 - Login")
            print("2 - Criar Conta")
            print("3 - Sair")
            op = input("Opção: ")

            if op == "1":
                user = login(usuarios)
            elif op == "2":
                criar_conta(usuarios)
            elif op == "3":
                break
        else:
            print(f"\n👤 Logado como: {user['nome']}")
            print("1 - Adicionar profissão")
            print("2 - Adicionar habilidades em uma profissão")
            print("3 - Ver perfil")
            print("4 - Logout")
            op = input("Opção: ")

            if op == "1":
                adicionar_profissao(user, usuarios)
            elif op == "2":
                adicionar_habilidades(user, usuarios)
            elif op == "3":
                ver_perfil(user)
            elif op == "4":
                user = None

main()
