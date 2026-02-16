import React from 'react';
import styles from './MovieModal.module.css';

export interface CastMember {
  id: number;
  name: string;
  character: string;
  profile_path: string | null;
  known_for_department: string;
}

interface CastCardProps {
  member: CastMember;
}

const CastCard: React.FC<CastCardProps> = ({ member }) => {
  return (
    <div className={styles.castCard}>
      {member.profile_path ? (
        <img src={member.profile_path} alt={member.name} />
      ) : (
        <div className={styles.noPhoto}>No Photo</div>
      )}
      <div className={styles.castInfo}>
        <p className={styles.actorName}>{member.name}</p>
        <p className={styles.characterName}>{member.character}</p>
        <span className={styles.department}>
          {member.known_for_department}
        </span>
      </div>
    </div>
  );
};

export default CastCard;