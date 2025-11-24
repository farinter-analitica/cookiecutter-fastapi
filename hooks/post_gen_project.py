#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Hook de post-generación para limpiar archivos innecesarios
basado en las opciones seleccionadas por el usuario.
"""
import os
import shutil
import sys
from pathlib import Path

# Configurar salida UTF-8 para Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')


def remove_file(filepath):
    """Elimina un archivo si existe"""
    if os.path.isfile(filepath):
        os.remove(filepath)
        print(f"[X] Removed: {filepath}")


def remove_dir(dirpath):
    """Elimina un directorio si existe"""
    if os.path.isdir(dirpath):
        shutil.rmtree(dirpath)
        print(f"[X] Removed directory: {dirpath}")


def create_dir(dirpath):
    """Crea un directorio si no existe"""
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
        print(f"[+] Created directory: {dirpath}")


def main():
    """Ejecuta la limpieza basada en las opciones del cookiecutter"""

    project_slug = "{{ cookiecutter.project_slug }}"
    project_type = "{{ cookiecutter.project_type }}"
    use_database = "{{ cookiecutter.use_database }}"
    use_workers = "{{ cookiecutter.use_workers }}"
    use_storage = "{{ cookiecutter.use_storage }}"
    use_ai_services = "{{ cookiecutter.use_ai_services }}"

    print("\n" + "="*60)
    print(f">> Configurando proyecto: {project_slug}")
    print(f">> Tipo de proyecto: {project_type}")
    print("="*60 + "\n")

    # Base paths
    app_path = Path("app")

    # =================================================================
    # LIMPIEZA SEGÚN TIPO DE PROYECTO
    # =================================================================

    # Si NO es un proyecto de ML/IA, eliminar carpetas relacionadas
    if project_type == "basic_api":
        print(">> Limpiando archivos de ML/IA (no necesarios)...")
        remove_dir(app_path / "ml")
        remove_file(app_path / "services" / "ml_service.py")
        remove_file(app_path / "services" / "predict.py")
        remove_file(app_path / "api" / "routes" / "predictor.py")

        # Eliminar tests de ML
        remove_file(Path("tests") / "test_api_predictor.py")
        remove_file(Path("tests") / "test_predict_service.py")
        remove_file(Path("tests") / "test_predictor.py")
        remove_file(Path("tests") / "test_ml_api.py")
        print("[OK] Configuracion para API basica completada\n")

    # =================================================================
    # LIMPIEZA DE SERVICIOS NO USADOS
    # =================================================================

    if use_workers == "no":
        print(">> Removiendo soporte para workers...")
        remove_dir(app_path / "workers")
        print("[OK] Workers removidos\n")

    if use_storage == "no":
        print(">> Removiendo servicios de almacenamiento...")
        remove_file(app_path / "services" / "storage_service.py")
        print("[OK] Servicios de almacenamiento removidos\n")

    if use_ai_services == "no":
        print(">> Removiendo servicios de IA...")
        remove_file(app_path / "services" / "ai_service.py")
        remove_file(app_path / "services" / "embed_service.py")
        remove_file(app_path / "services" / "chat_service.py")
        print("[OK] Servicios de IA removidos\n")

    # =================================================================
    # CREACION DE CARPETAS NECESARIAS
    # =================================================================

    print(">> Creando estructura de carpetas...")

    # Carpetas básicas siempre necesarias
    create_dir(app_path / "schemas")

    if use_database == "yes":
        create_dir(app_path / "models")
    else:
        # Si no hay base de datos pero es proyecto ML/IA, mantener models/prediction.py
        if project_type in ["ml_api", "ai_rag_api"]:
            # Solo eliminar archivos relacionados con DB, mantener prediction.py
            remove_file(app_path / "models" / "log.py")
            remove_file(app_path / "models" / "__init__.py")
        else:
            # Si no es ML/IA, eliminar todo models
            remove_dir(app_path / "models")
        remove_file(app_path / "db.py")

    if use_workers == "yes":
        create_dir(app_path / "workers")

    if use_storage == "yes":
        create_dir("uploads")

    # =================================================================
    # CREACION DE ARCHIVOS __init__.py
    # =================================================================

    print("\n>> Creando archivos __init__.py...")

    init_files = [
        app_path / "schemas" / "__init__.py",
    ]

    if use_database == "yes":
        init_files.append(app_path / "models" / "__init__.py")

    if use_workers == "yes":
        init_files.append(app_path / "workers" / "__init__.py")

    for init_file in init_files:
        if not init_file.exists():
            init_file.touch()
            print(f"[+] Created: {init_file}")

    # =================================================================
    # RESUMEN FINAL
    # =================================================================

    print("\n" + "="*60)
    print("[SUCCESS] Proyecto configurado exitosamente!")
    print("="*60)
    print("\n>> Configuracion aplicada:")
    print(f"   * Tipo: {project_type}")
    print(f"   * Base de datos: {use_database}")
    print(f"   * Workers: {use_workers}")
    print(f"   * Almacenamiento: {use_storage}")
    print(f"   * Servicios IA: {use_ai_services}")
    print("\n>> Proximos pasos:")
    print(f"   1. cd {project_slug}")
    print("   2. cp env.example .env")
    print("   3. Editar .env con tus credenciales")
    print("   4. docker-compose -f docker-compose.dev.yml up")
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()
