#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import os
import time
import logging
import argparse
from ftplib import FTP
import ftplib

def ftp_make_dir(ftp, dir_name, logger):
    """
    Crée un dossier sur le ftp.

    :param ftp: Serveur ftp.
    :param dir_name: Nom du dossier à créer.
    :param logger: Logger pour l'enregistrement des logs.
    """
    wd = ftp.pwd()
    dirs_list = dir_name.split('/')
    for folder in dirs_list:
        if folder not in ftp.nlst():
            try:
                ftp.mkd(folder)
            except:
                logger.debug('Could not create {0}.'.format(folder))
        ftp.cwd(folder)
    ftp.cwd(wd)


def ftp_rm_tree(ftp, path, logger):
    """
    Supprime récursivement un dossier et son contenu sur le ftp.

    :param ftp: Serveur ftp.
    :param path:  Nom du dossier à supprimer.
    :param logger: Logger pour l'enregistrement des logs.
    :return:
    """
    wd = ftp.pwd()
    try:
        names = ftp.nlst(path)
    except:
        return
    # Pour chaque fichier ou dossier contenu dans le dossier courant du ftp.
    for name in names:
        if os.path.split(name)[1] in ('.', '..'): continue
        try:
            # Si on peut s'y déplacer, c'est un dossier -> on revient au dossier de base sur le ftp
            # puis lance la méthode récursivement sur le dossier en question
            ftp.cwd(name)
            ftp.cwd(wd)
            ftp_rm_tree(ftp, name, logger)
        except:
            # Si c'est un fichier il n'y a qu'à le supprimer.
            ftp.delete(name)
    try:
        ftp.rmd(path)
        logger.info("The folder {0} has been deleted.".format(path))
    except:
        return


def ftp_add_file(ftp, name, local_file, logger):
    """
    Ajoute un fichier sur le serveur FTP en y inscrivant le contenu du fichier local.

    :param ftp: Serveur FTP.
    :param name: Chemin relatif du fichier à créer sur le ftp, depuis le dossier de base.
    :param local_file: Chemin local du fichier (relatif ou absolu)
    :param logger: Logger pour l'enregistrement des logs.
    """
    try:
        file = open(local_file, 'rb')
        ftp.storbinary('STOR {0}'.format(name), file)
        file.close()
    except IOError:
        logger.debug('Could not open local file {0}.'.format(local_file))
    except:
        logger.debug('Could not upload file {0}.'.format(name))


def ftp_delete_file(ftp, name, logger):
    """
    Supprime un fichier sur le serveur FTP.

    :param ftp: Serveur FTP.
    :param name: Chemin relatif du fichier à supprimer sur le ftp, depuis le dossier de base.
    :param logger: Logger pour l'enregistrement des logs.
    """
    try:
        ftp.delete(name)
    except:
        logger.debug('Could not delete file {0}. Maybe it was in a directory deleted beforehand?'.format(name))


def ftp_edit_file(ftp, name, local_file, logger):
    """
    Modifie un fichier sur le serveur FTP pour y inscrire le nouveau contenu du fichier local.

    :param ftp: Serveur FTP.
    :param name: Chemin relatif du fichier sur le FTP depuis le dossier de base.
    :param local_file: Chemin relatif ou absolu du fichier local.
    :param logger: Logger pour l'enregistrement des logs.
    """
    ftp_delete_file(ftp, name, logger)
    ftp_add_file(ftp, name, local_file, logger)


def ftp_move_file(ftp, old_name, new_name, logger):
    """
    Déplace un fichier sur le serveur FTP.

    :param ftp: Serveur FTP.
    :param old_name: Ancien nom du fichier.
    :param new_name: Nouveau nom du fichier.
    :param logger: Logger pour l'enregistrement des logs.
    """
    try:
        ftp.rename(old_name, new_name)
    except:
        logger.debug('Could not move file from {0} to {1}. Maybe it was moved with its parent directory beforehand?'.format(old_name, new_name))


def folder_added(name, logger, ftp, ref_directory):
    """
    Lance l'ajout d'un dossier sur le ftp.

    :param name: Nom relatif ou absolu du dossier à ajouter.
    :param logger: Logger pour l'enregistrement des logs.
    :param ftp: Serveur FTP.
    :param ref_directory: Répertoire de référence.
    """
    ftp_make_dir(ftp, name[len(ref_directory) + 1:], logger)
    logger.info('The folder {0} has been created.'.format(name))


def folder_deleted(name, logger, ftp, ref_directory):
    """
    Lance la suppression d'un dossier sur le FTP.

    :param name: Nom relatif ou absolu du dossier à supprimer.
    :param logger: Logger pour l'enregistrement des logs.
    :param ftp: Serveur FTP.
    :param ref_directory: Répertoire de référence.
    """
    ftp_rm_tree(ftp, name[len(ref_directory) + 1:], logger)
    logger.info('The folder {0} has been deleted.'.format(name))


def folder_moved(old_name, new_name, logger, ftp, ref_directory):
    """
    Lance le déplacement d'un dossier sur le FTP.

    :param old_name: Ancien nom relatif ou absolu du dossier.
    :param new_name: Nouveau nom relatif ou absolu du dossier.
    :param logger: Logger pour l'enregistrement des logs.
    :param ftp: Serveur FTP.
    :param ref_directory: Répertoire de référence.
    """
    ftp_rm_tree(ftp, old_name[len(ref_directory) + 1:], logger)
    ftp_make_dir(ftp, new_name[len(ref_directory) + 1:], logger)
    new_folder = ({}, {})
    fill_directories_dictionary(new_folder[0], new_folder[1], new_name)
    for path in new_folder[0].values():
        ftp_make_dir(ftp, path[len(ref_directory) + 1:], logger)
    for file in new_folder[1].values():
        logger.info('Trying to add file {0}...'.format(file))
        ftp_add_file(ftp, file[0][len(ref_directory) + 1:], file[0], logger)
    logger.info('The folder {0} was moved to {1}.'.format(old_name, new_name))


def file_modified(name, logger, ftp, ref_directory):
    """
    Lance la modification d'un fichier sur le serveur FTP.

    :param name: Nom relatif ou absolu du fichier.
    :param logger: Logger pour l'enregistrement des logs.
    :param ftp: Serveur FTP.
    :param ref_directory: Répertoire de référence.
    """
    ftp_edit_file(ftp, name[len(ref_directory) + 1:], name, logger)
    logger.info('The file {0} has been modified.'.format(name))


def file_added(name, logger, ftp, ref_directory):
    """
    Lance l'ajout d'un fichier sur le serveur FTP.

    :param name: Nom relatif ou absolu du fichier.
    :param logger: Logger pour l'enregistrement des logs.
    :param ftp: Serveur FTP.
    :param ref_directory: Répertoire de référence.
    """
    ftp_add_file(ftp, name[len(ref_directory) + 1:], name, logger)
    logger.info('The file {0} has been created.'.format(name))


def file_deleted(name, logger, ftp, ref_directory):
    """
    Lance la suppression d'un fichier sur le serveur FTP.

    :param name: Nom relatif ou absolu du fichier à supprimer.
    :param logger: Logger pour l'enregistrement des logs.
    :param ftp: Serveur FTP.
    :param ref_directory: Répertoire de référence.
    """
    ftp_delete_file(ftp, name[len(ref_directory) + 1:], logger)
    logger.info('The file {0} has been deleted.'.format(name))


def file_moved(old_name, new_name, logger, ftp, ref_directory):
    """
    Lance le déplacement d'un fichier sur le serveur FTP.

    :param old_name: Ancien nom relatif ou absolu du fichier.
    :param new_name: Nouveau nom relatif ou absolu du fichier.
    :param logger: Logger pour l'enregistrement des logs.
    :param ftp: Serveur FTP.
    :param ref_directory: Répertoire de référence.
    """
    ftp_move_file(ftp, old_name[len(ref_directory) + 1:], new_name[len(ref_directory) + 1:], logger)
    logger.info("The  file  {0} has been moved to {1}.".format(old_name, new_name))


def folder_analyse(old_state, new_state, logger, ftp, ref_directory):
    """
    Analyse les deux dictionnaires de dossiers en comparant les entrées.

    :param old_state: Dictionnaire d'ancien état.
    :param new_state: Dictionnaire de nouvel état.
    :param logger: Logger pour l'enregistrement des logs.
    :param ftp: Serveur FTP.
    :param ref_directory: Répertoire de référence.
    """
    for node in new_state.keys():
        if node in old_state.keys():
            old_name = old_state[node]
            new_name = new_state[node]
            if old_name != new_name:
                folder_moved(old_name, new_name, logger, ftp, ref_directory)
        else:
            folder_added(new_state[node], logger, ftp, ref_directory)
    for node in old_state.keys():
        if node not in new_state.keys():
            folder_deleted(old_state[node], logger, ftp, ref_directory)


def files_analyse(old_state, new_state, logger, ftp, ref_directory):
    """
    Analyse les deux dictionnaires de fichiers en comparant les entrées.

    :param old_state: Dictionnaire d'ancien état.
    :param new_state: Dictionnaire de nouvel état.
    :param logger: Logger pour l'enregistrement des logs.
    :param ftp: Serveur FTP.
    :param ref_directory: Répertoire de référence.
    """
    for node in new_state.keys():
        if node in old_state.keys():
            old_name = old_state[node][0]
            new_name = new_state[node][0]
            if new_name == old_name:
                old_time = old_state[node][1]
                new_time = new_state[node][1]
                if old_time != new_time:
                    file_modified(new_name, logger, ftp, ref_directory)
            else:
                file_moved(old_name, new_name, logger, ftp, ref_directory)
        else:
            file_added(new_state[node][0], logger, ftp, ref_directory)
    for node in old_state.keys():
        if node not in new_state.keys():
            file_deleted(old_state[node][0], logger, ftp, ref_directory)


def fill_files_dictionary(dictionary, folder, files):
    """
    Remplie le dictionaire de fichiers à partir d'une liste de fichiers dans un répertoire donné.

    :param dictionary: Le dictionnaire à remplire.
    :param folder: Le dossier dont il faut lister le contenu.
    :param files: Les fichiers à intégrer dans le dictionnaire.
    """
    for file in files:
        full_path = os.path.join(folder, file)
        # Récupération du timestamp de dernière modification
        timestamp = int(os.path.getmtime(full_path))
        inode = int(os.stat(full_path).st_ino)
        dictionary[inode] = (full_path, timestamp)


def fill_directories_dictionary(dictionary_folders, dictionary_files, folder):
    """
    Remplie deux dictionnaires de dossiers et fichiers à partir d'un dossier racine.

    :param dictionary_folders: Dictionnaire de dossiers.
    :param dictionary_files: Dictionnaire de fichiers.
    :param folder: Dossier racine dont on veut lister le contenu.
    """

    print('fill directories dictionary')
    for root, dirs, files in os.walk(folder):
        fill_files_dictionary(dictionary_files, root, files)
        inode = int(os.stat(root).st_ino)
        dictionary_folders[inode] = root


def run1(args, logger, ftp):
    """
    Procède à la synchronisation.

    :param args: Les arguments rentrés par l'utilisateur
    :param logger: Logger pour l'enregistrement des logs.
    :param ftp: Serveur FTP.
    """
    old_state = ({}, {})
    fill_directories_dictionary(old_state[0], old_state[1], args.directory)
    while 1 == 1:
        time.sleep(args.time)
        new_state = ({}, {})
        fill_directories_dictionary(new_state[0], new_state[1], args.directory)
        folder_analyse(old_state[0], new_state[0], logger, ftp, args.directory)
        files_analyse(old_state[1], new_state[1], logger, ftp, args.directory)
        old_state = new_state


def run(ftp,directory,logger):
    old_state = ({}, {})
    fill_directories_dictionary(old_state[0], old_state[1], directory)
    new_state = ({}, {})
    while 1 == 1:
        time.sleep(2)
        fill_directories_dictionary(new_state[0], new_state[1], directory)
        folder_analyse(old_state[0], new_state[0], logger, ftp, directory)
        files_analyse(old_state[1], new_state[1], logger, ftp, directory)
        old_state = new_state

def main():
    
    ftp = FTP()
    # ftp.connect('ftp.brender.cn',22122)
    # ftp.connect('182.92.200.86',22123)
    ftp.connect('192.168.1.123',22123)
    ftp.login('user','12345')

    # ftp = ftplib.FTP('182.92.200.86',22122)
    # ftp.login("user", "12345")
    print(ftp.getwelcome())
    # ftp.cwd(remote_dir)

    print(ftp.pwd())
    print(ftp.nlst())
    ftp.quit()
    
main()