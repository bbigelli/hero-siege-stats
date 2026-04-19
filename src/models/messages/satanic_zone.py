from src.models.messages.base import BaseMessage
from src.consts.satanic_buffs import satanic_buffs
from src.consts.satanic_debuffs import satanic_debuffs
from src.consts.satanic_zone_names import satanic_zone_names
from src.utils import assets
from src.consts import assets as assets_const

# Converte os dicionários em listas para acesso por índice
def create_id_mapping(buffs_dict):
    """
    Cria um mapeamento de ID para nome baseado na ordem do dicionário.
    IDs começam em 1 (primeiro item = ID 1)
    """
    if not buffs_dict:
        return {}
    
    # Se for dicionário, pega as chaves (nomes)
    if isinstance(buffs_dict, dict):
        buff_names = list(buffs_dict.keys())
    else:
        buff_names = buffs_dict
    
    # Cria mapeamento (ID 1 = primeiro nome, ID 2 = segundo nome, etc.)
    return {idx + 1: name for idx, name in enumerate(buff_names)}

# Criar mapeamentos automaticamente
buff_id_to_name = create_id_mapping(satanic_buffs)
debuff_id_to_name = create_id_mapping(satanic_debuffs)


class SzBuff:
    buff_name: str
    buff_description: str | None
    buff_icon: str
    is_negative: bool
    
    def __init__(self, sz_buff: int, is_negative: bool = False):
        self.is_negative = is_negative
        
        if is_negative:
            # Buscar debuff pelo ID no mapeamento
            if sz_buff in debuff_id_to_name:
                self.buff_name = debuff_id_to_name[sz_buff]
                self.buff_description = satanic_debuffs.get(self.buff_name, "Unknown debuff effect")
            else:
                self.buff_name = f"Unknown Debuff (ID: {sz_buff})"
                self.buff_description = "Unknown debuff effect"
        else:
            # Buscar buff pelo ID no mapeamento
            if sz_buff in buff_id_to_name:
                self.buff_name = buff_id_to_name[sz_buff]
                self.buff_description = satanic_buffs.get(self.buff_name, f"Buff effect: {self.buff_name}")
            else:
                self.buff_name = f"Unknown Buff (ID: {sz_buff})"
                self.buff_description = "Unknown buff effect"
        
        # Carregar ícone
        if is_negative:
            # Tentar carregar ícone de debuff primeiro
            debuff_icon_name = f"IcDebuff_{sz_buff}"
            if hasattr(assets_const, debuff_icon_name):
                buff_icon_path = getattr(assets_const, debuff_icon_name)
            else:
                buff_icon_path = getattr(assets_const, 'IcDebuffDefault', assets_const.IcBuffDefault)
        else:
            # Carregar ícone de buff
            buff_icon_name = f"IcBuff_{sz_buff}"
            if hasattr(assets_const, buff_icon_name):
                buff_icon_path = getattr(assets_const, buff_icon_name)
            else:
                buff_icon_path = assets_const.IcBuffDefault
        
        self.buff_icon = assets.icon(buff_icon_path)


class SzInfo:
    positive_buffs: list
    negative_buffs: list
    satanic_zone: str
    
    def __init__(self, sz_zone: str, sz_buffs: str, sz_negative_buffs: str = ""):
        self.positive_buffs = []
        self.negative_buffs = []
        
        # Processar buffs positivos
        if sz_buffs:
            for buff in sz_buffs.split("|"):
                if buff and buff.strip():
                    buff_id = int(buff)
                    b = SzBuff(buff_id, is_negative=False)
                    self.positive_buffs.append(b)
        
        # Processar debuffs (negativos)
        if sz_negative_buffs:
            for debuff in sz_negative_buffs.split("|"):
                if debuff and debuff.strip():
                    debuff_id = int(debuff)
                    b = SzBuff(debuff_id, is_negative=True)
                    self.negative_buffs.append(b)
        
        # Processar zona satânica
        temp = sz_zone.split("_")
        if len(temp) >= 3:
            try:
                sz_act: int = int(temp[1])
                sz_zone_name_id: int = int(temp[2])
                all_act_zone_names_of_id: list | None = satanic_zone_names.get(sz_act)
                if all_act_zone_names_of_id and sz_zone_name_id - 1 < len(all_act_zone_names_of_id):
                    sz_zone_name = all_act_zone_names_of_id[sz_zone_name_id - 1]
                    self.satanic_zone = f"Act {sz_act} : {sz_zone_name}"
                else:
                    self.satanic_zone = ""
            except (ValueError, IndexError):
                self.satanic_zone = ""
        else:
            self.satanic_zone = ""


class SatanicZoneMessage(BaseMessage):
    satanic_info: SzInfo
    
    def __init__(self, msg_dict: dict):
        super().__init__(msg_dict)
        negative_buffs = msg_dict.get('negativeBuffs', msg_dict.get('debuffs', msg_dict.get('negative_buffs', '')))
        
        self.satanic_info = SzInfo(
            msg_dict.get('satanicZoneName', ''),
            msg_dict.get('buffs', ''),
            negative_buffs
        )